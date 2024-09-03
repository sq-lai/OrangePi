# -*- coding: utf-8 -*-
import os
import subprocess

# UI文件所在的路径
input_dir = 'UI'  # 当前目录,要用相对路径
# 转换后的py文件保存路径
output_dir = 'UI'  # 你可以指定你希望保存的路径

# 检查并创建输出目录
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 检查 pyuic5 是否可用
def check_pyuic5():
    try:
        result = subprocess.run(['pyuic5', '--version'], check=True, capture_output=True, text=True)
        print("pyuic5 is available. Version:", result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print("pyuic5 command failed:", e)
        return False
    except FileNotFoundError:
        print("pyuic5 is not installed or not in PATH.")
        return False

# 列出目录下的所有ui文件
def list_ui_files(directory):
    ui_files = []
    try:
        files = os.listdir(directory)
        for filename in files:
            if os.path.splitext(filename)[1] == '.ui':
                ui_files.append(os.path.join(directory, filename))
    except Exception as e:
        print(f"Error listing files in directory {directory}: {e}")
    return ui_files

# 把后缀为ui的文件改成后缀为py的文件名
def trans_py_file(ui_filepath, output_directory):
    base_name = os.path.splitext(os.path.basename(ui_filepath))[0]
    return os.path.join(output_directory, base_name + '.py')

# 调用系统命令把ui转换成py
def convert_ui_to_py(input_directory, output_directory):
    ui_files = list_ui_files(input_directory)
    if not ui_files:
        print("No .ui files found in the directory.")
        return

    for uifile in ui_files:
        pyfile = trans_py_file(uifile, output_directory)
        cmd = ['pyuic5', '-o', pyfile, uifile]
        print(f"Running command: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True)
            print(f"Converted {uifile} to {pyfile}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting {uifile}: {e}")

###### 程序的主入口
if __name__ == "__main__":
    if check_pyuic5():
        convert_ui_to_py(input_dir, output_dir)
    else:
        print("Please install PyQt5 and ensure pyuic5 is in your PATH.")
