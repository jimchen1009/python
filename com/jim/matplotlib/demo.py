#导入必要的模块
import matplotlib.pyplot as plt


#录入身高与体重数据
height = ['170', '179', '159', '160', '180', '164', '168', '174', '160', '183']
weight = ['57', '62', '47', '67', '59', '49', '54', '63', '66', '80']

plt.scatter(height, weight, s=40, c='r',  marker='.')     #散点图生成
plt.xlabel('height(cm)')                             # plt.xlabel 设置x轴标签
plt.ylabel('weight(kg)')                             # plt.ylabel 设置y轴标签
plt.title('demo')                                    #plt.title  设置图像标题

plt.grid()
plt.show()                                           #显示图片