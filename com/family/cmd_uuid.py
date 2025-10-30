# Step 1: 从文件1中提取关键字A
def extract_key_from_file1(file1_path):
    keys = []
    with open(file1_path, 'r') as file1:
        for line in file1:
            if '13/3' in line:
                # 提取关键字A
                key = line.split('/')[-1].strip()
                keys.append(key)
    return keys


# Step 2: 在文件2中过滤并统计
def count_key_in_file2(file2_path, keys):
    key_count = {key: 0 for key in keys}

    with open(file2_path, 'r') as file2:
        for line in file2:
            for key in keys:
                if key in line:
                    key_count[key] += 1

    return key_count


# 主程序
if __name__ == "__main__":
    file1_path = 'C:Users/chenjingjun/Desktop/op_upload_20250410122550_361/prof/game1001_prof_detail_2025-04-10-12.log'
    file2_path = 'C:/Users/chenjingjun/Desktop/op_upload_20250410122550_361/redis/game1001_redis_2025-04-10-12.log'

    # 提取关键字A
    keys = extract_key_from_file1(file1_path)

    # 在文件2中统计
    key_count = count_key_in_file2(file2_path, keys)

    # 排序结果，按计数降序排列
    sorted_key_count = sorted(key_count.items(), key=lambda item: item[1], reverse=True)

    # 输出结果
    for key, count in key_count.items():
        print(f'Key: {key}, Count: {count}')
