# WriteToJson
根据地图文件生成（csv/lpx）生成json配置文件的脚本，适用于EPSILON代码的lane_net_norm.json格式。

# Introduction
lane_net_norm.json为原EPSILON代码中的车道线配置文件；
lane_net_norm_2.json为新生成的车道线配置文件；
demo.csv为原始路径文件；


# Usage
1.修改main()函数中的loading_data地址，data = loading_data(file_path, 'demo.csv')；
2.python main.py raw_path/
