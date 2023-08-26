# https://github.com/Anlv-max/C4D_Anlv_Script
# Works With Cinema 4D 2023.2.2
# USE AT YOUR OWN RISK

"""
Name-US:Collect Tex
Name-ZH:收集贴图
Description-US:Copy the linked textures to the tex folder of the project, and modify them to relative paths.
Description-ZH:将已链接的贴图复制到项目的tex文件夹，同时修改为相对路径。
"""

import c4d
import os
import shutil

# 使用相对路径还是绝对路径
use_relative_path = True  # 在这里设置

# 遍历材质的所有子节点
def iterate_shader(shader, tex_dir, doc_dir):
    while shader:
        if shader.CheckType(1029508):  # Octane ImageTexture节点
            old_path = shader[c4d.IMAGETEXTURE_FILE]
            filename = os.path.basename(old_path)
            new_path = os.path.join(tex_dir, filename)

            # 如果选择使用相对路径
            if use_relative_path:
                new_path = os.path.relpath(new_path, doc_dir)

            shader[c4d.IMAGETEXTURE_FILE] = new_path
        if shader.GetDown():
            iterate_shader(shader.GetDown(), tex_dir, doc_dir)
        shader = shader.GetNext()

# 主函数
def main():
    doc = c4d.documents.GetActiveDocument()
    doc_path = doc[c4d.DOCUMENT_FILEPATH]
    doc_dir = os.path.dirname(doc_path)

    if not doc_dir:
        c4d.gui.MessageDialog('请先保存当前项目!')
        return

    # 创建tex文件夹
    tex_dir = os.path.join(doc_dir, 'tex')
    if not os.path.exists(tex_dir):
        os.makedirs(tex_dir)

    # 收集贴图
    assetList = []
    c4d.documents.GetAllAssetsNew(doc, False, "", c4d.ASSETDATA_FLAG_TEXTURESONLY, assetList)
    texture_paths = [asset['filename'] for asset in assetList if asset['exists']]
    
    copied_count = 0
    for path in texture_paths:
        filename = os.path.basename(path)
        dest_path = os.path.join(tex_dir, filename)
        if os.path.abspath(path) != os.path.abspath(dest_path):
            shutil.copy2(path, dest_path)
            copied_count += 1

    # 更新Octane ImageTexture节点路径
    materials = doc.GetMaterials()
    for mat in materials:
        first_shader = mat.GetFirstShader()
        iterate_shader(first_shader, tex_dir, doc_dir)

    message = f'贴图已经收集并更新完成!\n已复制：{copied_count}'
    c4d.gui.MessageDialog(message)
    c4d.EventAdd()

# 执行主函数
if __name__=='__main__':
    main()

    