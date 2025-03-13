import subprocess   
from program.common import convert_to_readable , cipher_algorithm_mapping_name, integrity_algorithm_mapping_name, get_tshark_output ,security_header_mapping_name, prompt_creator
from program.chatgpt import chatgpt_response
from program.gemini import gemini_response 

def security_mode_command_factor_retrieve_text(uplink_command, downlink_command, key_estbl_status, message_encoding_type, pcap_file_path, dl_com_invoke_line):
    pcap_file = pcap_file_path
    
    abba_field = 'nas_5gs.mm.abba_contents'
    cipher_algorithm_field = 'nas_5gs.mm.nas_sec_algo_enc'
    integrity_algorithm_field = 'nas_5gs.mm.nas_sec_algo_ip'
    security_header_field = 'nas_5gs.security_header_type'
    
    abba = get_tshark_output(pcap_file, abba_field, dl_com_invoke_line)
    cipher_algorithm = get_tshark_output(pcap_file, cipher_algorithm_field, dl_com_invoke_line)
    integrity_algorithm = get_tshark_output(pcap_file, integrity_algorithm_field, dl_com_invoke_line)
    header = get_tshark_output(pcap_file, security_header_field, dl_com_invoke_line)
    
    first_part = None  # Initialize first_part outside the if statement

    if key_estbl_status:
        key_estbl_status_str = 'Completed'
    else:
        key_estbl_status_str = 'Not completed yet'

    factor_text = (
        'Uplink message from the UE: ' + convert_to_readable(uplink_command) + '\n' +
        'Subsequent Downlink message from the AMF: ' + convert_to_readable(downlink_command) + '\n' +
        'The downlink message from the AMF was sent as: ' + message_encoding_type + '\n' +
        '5G-AKA: ' + key_estbl_status_str + '\n'
    )
    
    if abba is not None and abba.strip():
        factor_text += 'ABBA: ' + str(abba) + '\n'

    if cipher_algorithm is not None and cipher_algorithm.strip():
        cipher_algorithm_name = cipher_algorithm_mapping_name(int(cipher_algorithm))
        factor_text += 'Cipher Algorithm: ' + cipher_algorithm_name + '\n'

    if integrity_algorithm is not None and integrity_algorithm.strip():
        integrity_algorithm_name = integrity_algorithm_mapping_name(int(integrity_algorithm))
        factor_text += 'Integrity Algorithm: ' + integrity_algorithm_name + '\n'
        
    if header is not None and header.strip():
        parts = header.split(',')

        if parts:
            first_part = parts[0]
            name = security_header_mapping_name(str(first_part))
            factor_text += 'Security header: ' + name + '\n'

    return factor_text
    
    
    
def security_mode_command_part(factor_to_consider, uplink_command, downlink_command ,response, pcap_file_path,dl_com_invoke_line, renamed_pcap_text,llm_type):
    key_estbl_status = factor_to_consider[0]
    message_encoding_type = factor_to_consider[1]  
    factor_text = security_mode_command_factor_retrieve_text(uplink_command, downlink_command, key_estbl_status, message_encoding_type,pcap_file_path,dl_com_invoke_line)
    full_prompt = prompt_creator(downlink_command, uplink_command,response,factor_text, renamed_pcap_text)
    if llm_type == "chatgpt":
        chatgpt_answer, status = chatgpt_response(full_prompt)
        return full_prompt, chatgpt_answer, status
    elif llm_type == "gemini":
        gemini_answer, status = gemini_response(full_prompt)
        return full_prompt, gemini_answer, status
    else:
        raise ValueError(f"Invalid llm_type: {llm_type}. Expected 'chatgpt' or 'gemini'.")
        return None, None, None
