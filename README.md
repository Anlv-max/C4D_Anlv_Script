[![Twitter](https://github.com/Anlv-max/C4D_Anlv_Script/raw/main/img/Twitter.png)](https://twitter.com/Anlv_Max)  

**注意：**   
这些脚本是为 Cinema 4D 2023.2.2 编写的。在 Microsoft Windows 10 上进行了测试。
使用这些脚本需要自担风险！  


**特别鸣谢**  
Aturtur https://github.com/aturtur  
Lasselauch https://github.com/lasselauch  
MikeUdin https://github.com/MikeUdin  
  
这里收集的脚本中存在对以上作者脚本代码的借鉴或引用，我也是因为使用了 aturtur Cinema 4D 脚本后对脚本的编写产生了兴趣，对此非常感谢这些作者的分享。  

----

![Add MoGraph Cache tag](https://github.com/Anlv-max/C4D_Anlv_Script/blob/main/img/script%20icon/Add%20MoGraph%20Cache%20tag.png?raw=true)   
#### Add MoGraph Cache Tag  
**Default :** Add MoGraph Cache Tag To All Motion Graphic Objects In The Scene.  
#### 添加运动图形缓存标签  
**默认 :** 为场景中的所有运动图形对象添加运动图形缓存标签.  

![Axis Center](https://github.com/Anlv-max/C4D_Anlv_Script/blob/main/img/script%20icon/Axis%20Center.png?raw=true)  
#### Axis Center  
**Default :** The selected object is centered on the axis.  
**Shift-click :** The axis of the selected object is placed at the bottom  
#### 轴心控制  
**默认 :** 选中的对象轴心居中。  
**Shift-click ：** 选中的对象轴心置于底部 

![CNV Conversion Subdivision](https://github.com/Anlv-max/C4D_Anlv_Script/blob/main/img/script%20icon/CNV%20Conversion%20Subdivision.png?raw=true)  
#### CNV Conversion Subdivision  
**Default :** Convert all subdivided surface objects to Octane Object tag and add subdivision.  
#### CNV 细分对象转换器  
**默认 :** 将「细分对象」转换为「Octane 对象标签」并开启细分。（细分等级根据细分对象嵌套数设置，如未选中对象，则对整个场景进行转换。）  

![Clean Curve](https://github.com/Anlv-max/C4D_Anlv_Script/blob/main/img/script%20icon/Clean%20Curve.png?raw=true)  
#### Clean Curve  
**Default :** Clean selected curves  
**Shift+click :** Clean the entire scene
**Ctrl+click :** Clean the entire scene, excluding selected objects.  
#### 清洁动画曲线  
**默认:** 清洁选中对象的无效曲线  
**Shift+click :** 清洁整个场景  
**Ctrl+click :** 清洁整个场景，但排除选中对象  

![Collect Tex](https://github.com/Anlv-max/C4D_Anlv_Script/blob/main/img/script%20icon/Collect%20Tex.png?raw=true)  
#### Collect Tex  
**Default :** Copy the linked textures to the tex folder of the project, and modify them to relative paths.  
#### 收集贴图  
**默认 :** 将已链接的贴图复制到项目的tex文件夹，同时修改为相对路径。  

![Copy Object](https://github.com/Anlv-max/C4D_Anlv_Script/blob/main/img/script%20icon/Copy%20Object.png?raw=true)  
#### Copy Object  
**Default :** Copy the currently selected object.  
#### 复制对象  
**默认 :** 拷贝一份当前选中的对象.  

![Del Protection Tag](https://github.com/Anlv-max/C4D_Anlv_Script/blob/main/img/script%20icon/Del%20Protection%20Tag.png?raw=true)  
#### Del Protection Tag  
**Default :** Remove All Protection Tag In The Scene.  
#### 删除保护标签  
**默认 :** 删除场景中所有的保护标签  

![Delete Null](https://github.com/Anlv-max/C4D_Anlv_Script/blob/main/img/script%20icon/Delete%20Null.png?raw=true)  
#### Delete Null Objects  
**Default :** Delete Null objects that do not contain child elements in the scene.  
#### 删除空对象  
**默认 :** 删除场景中不包含子级的空对象.  

![Mute Layer](https://github.com/Anlv-max/C4D_Anlv_Script/blob/main/img/script%20icon/Mute%20Layer.png?raw=true)  
#### Mute Layer  
**Default :** CLOSE View\Render\Manager\Locked\Animation\Generators\Deformers\Expressions\Xref  
#### 静音层  
**默认 :** 关闭 View\Render\Manager\Locked\Animation\Generators\Deformers\Expressions\Xref  

![Select Same Object Type](https://github.com/Anlv-max/C4D_Anlv_Script/blob/main/img/script%20icon/Select%20Same%20Object%20Type.png?raw=true)  
#### Act on same Object-Types  
**Default :** Select same Object-Types  
**Ctrl-click :** Turn same Object-Types to OFF
**Alt-click :** Turn same Object-Types to DEFAULT  
#### 选择相同的对象类型  
**默认 :** 选择相同的对象类型  
**Ctrl-click :** 将相同的对象类型设置为关闭  
**Alt-CLICK :** 将相同的对象类型设置为默认  

![Select Same Tag](https://github.com/Anlv-max/C4D_Anlv_Script/blob/main/img/script%20icon/Select%20Same%20Tag.png?raw=true)  
#### Act on same TAG-Types  
**Default:** Click the button after selecting a tag, and select tags of the same type.  
#### 选择相同标签  
**默认 :** 选中一个标签后点击左键，将选中相同类型的标签。  

----
## 安装：

要安装这些脚本，请按照以下步骤进行：  

1. 下载此存储库并解压缩。   
2. 将"Anlv Script"文件夹复制到以下路径：   
   **Windows：**  
   `C:\Users\<USER>\AppData\Roaming\MAXON\Maxon Cinema 4D RXX\library\scripts`  
   **Mac OS：**  
   `/Applications/MAXON/CINEMA 4D RXX/library/scripts`  
	 如果您不确定如何找到安装脚本的文件夹，请打开Cinema 4D并转到首选项。然后点击"打开首选项文件夹..."按钮，然后导航到"库 > 脚本"文件夹。

确保将脚本放置在正确的位置，并重新启动Cinema 4D。现在，您应该能够在Cinema 4D中访问和使用这些脚本了。

如果您在使用这些脚本时遇到任何问题，请随时联系我。感谢您的支持！
