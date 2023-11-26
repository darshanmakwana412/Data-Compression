import os
import pickle
import gradio as gr
from huffman import *

def compress(file_path, status):
    global forward,reverse
    filename = os.path.splitext(file_path)[0]
    output_path = str(filename) + ".hzip"
    with open(file_path, 'r+', encoding="utf-8") as input_file, open(output_path, 'wb') as output_file, open("archive/eileen", 'wb') as new_output_file:
        text = input_file.read()
        status += "Creating Huffman Codes.\n"
        h = get_heap(text)
        tree = generate_tree(h)
        generate_code(tree,'')
        status += "Encoding File.\n"
        encoded_text, buffer = encode(text,forward)
        metadata_obj = metadata(reverse,encoded_text,buffer)
        pickle.dump(list(reverse.items()), new_output_file)
        pickle.dump(metadata_obj, output_file, pickle.HIGHEST_PROTOCOL)
        status += "Finished Encoding File.\n"
    return output_path, status

def decompress(file_d, status):
    filename = os.path.splitext(file_d)[0]
    output_path = filename + ".txt"
    with open(file_d, 'rb') as input_file, open(output_path, 'w', encoding='utf-8') as output_file:
        status += "Exctracting Metadata.\n"
        data = pickle.load(input_file)
        status += "Decoding Bytes to Text\n"
        text = decode(data.codex, data.encoded_text, data.buffer)
        status += "Writing to File.\n"
        output_file.write(text)
    return output_path, status

def main():
    with gr.Blocks() as app:
        gr.Markdown("# Data Compression using Huffman Codes")

        with gr.Row():
            with gr.Column():
                action = gr.Dropdown(choices=["Compress", "Decompress"], label="Action")
                file_input = gr.File(label="Upload your Text File")
                submit_button = gr.Button("Submit")
            
            with gr.Column():
                status = gr.Textbox(label="Status", interactive=False)
                result = gr.File(label="Download")

        # Gradio interface
        def process_file(action, file_obj):

            mssg = ""
            result_file = ""

            if action == "Compress":
                if(os.path.isfile(file_obj.name)):
                    extension = os.path.splitext(file_obj.name)[1]
                    if(extension != '.hzip'):
                        mssg += "Compressing data...\n"
                        result_file, mssg = compress(file_obj.name, mssg)
                        mssg += "Finished compressing data.\n"
                    else:
                        mssg += "File is already compressed.\n"
                else:
                    mssg += "File does not exist.\n"
            else:

                if(os.path.isfile(file_obj.name)):
                    extension = os.path.splitext(file_obj.name)[1]
                    if(extension == '.hzip'):
                        mssg += "Decompressing data...\n"
                        result_file, mssg = decompress(file_obj.name, mssg)
                        mssg += "Finished decompressing data.\n"
                    else:
                        mssg += "Enter a valid .hzip file.\n"
                else:
                    mssg += "File does not exist.\n"

            return result_file, mssg

        submit_button.click(
            fn=process_file, 
            inputs=[action, file_input],
            outputs=[result, status]
        )

    app.launch(share=True)

if __name__ == "__main__":
    main()