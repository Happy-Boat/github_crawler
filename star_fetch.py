import requests
import json


def fetch_and_save_data():
    page = 1
    all_data = []
    while True:
        api_url = f'https://api.github.com/users/hwfan/starred?per_page=100&page={page}'
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            if not data:
                break
            all_data.extend(data)
            page = page + 1
        except requests.RequestException as e:
            print(f'请求出错: {e}')
            break
        except json.JSONDecodeError as e:
            print(f'JSON 解析出错: {e}')
            break
        except Exception as e:
            print(f'发生未知错误: {e}')
            break

    try:
        with open('star.json', 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)
        print('数据已成功保存到star.json 文件中。')
    except Exception as e:
        print(f'保存文件时出错: {e}')


if __name__ == "__main__":
    fetch_and_save_data()