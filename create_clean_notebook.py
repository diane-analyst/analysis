import json

def create_clean_notebook(source_file):
    """노트북 파일을 완전히 깨끗한 구조로 재생성합니다."""
    print(f"\n=== {source_file} 깨끗하게 재생성 ===\n")
    
    # 원본 읽기
    with open(source_file, 'r', encoding='utf-8') as f:
        source_data = json.load(f)
    
    # 완전히 새로운 깨끗한 노트북 생성
    clean_notebook = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    # 각 셀을 깨끗하게 재구성
    for cell in source_data.get('cells', []):
        cell_type = cell.get('cell_type', 'code')
        
        # source 정리
        source_list = []
        source = cell.get('source', [])
        
        if isinstance(source, str):
            source_list = source.split('\n')
        elif isinstance(source, list):
            for line in source:
                if line is None:
                    continue
                if isinstance(line, str):
                    source_list.append(line)
                else:
                    source_list.append(str(line))
        else:
            source_list = ['']
        
        # 빈 리스트 처리
        if not source_list:
            source_list = ['']
        
        # 마지막 빈 줄 제거
        while len(source_list) > 1 and source_list[-1] == '':
            source_list.pop()
        
        # 새 셀 생성
        if cell_type == 'markdown':
            new_cell = {
                "cell_type": "markdown",
                "metadata": {},
                "source": source_list
            }
        else:  # code
            new_cell = {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": source_list
            }
            
            # outputs 처리 (매우 신중하게)
            old_outputs = cell.get('outputs', [])
            if isinstance(old_outputs, list):
                for output in old_outputs:
                    if not isinstance(output, dict):
                        continue
                    
                    output_type = output.get('output_type')
                    if not output_type:
                        continue
                    
                    # execute_result
                    if output_type == 'execute_result':
                        data = output.get('data', {})
                        if isinstance(data, dict) and data:
                            new_output = {
                                "output_type": "execute_result",
                                "execution_count": None,
                                "data": {}
                            }
                            for key, value in data.items():
                                if key and value is not None:
                                    if isinstance(value, str):
                                        new_output['data'][key] = value
                                    elif isinstance(value, list):
                                        cleaned = [str(v) for v in value if v is not None]
                                        if cleaned:
                                            new_output['data'][key] = cleaned
                                    else:
                                        new_output['data'][key] = str(value)
                            if new_output['data']:
                                new_cell['outputs'].append(new_output)
                    
                    # display_data
                    elif output_type == 'display_data':
                        data = output.get('data', {})
                        if isinstance(data, dict) and data:
                            new_output = {
                                "output_type": "display_data",
                                "data": {}
                            }
                            for key, value in data.items():
                                if key and value is not None:
                                    if isinstance(value, str):
                                        new_output['data'][key] = value
                                    elif isinstance(value, list):
                                        cleaned = [str(v) for v in value if v is not None]
                                        if cleaned:
                                            new_output['data'][key] = cleaned
                                    else:
                                        new_output['data'][key] = str(value)
                            if new_output['data']:
                                new_cell['outputs'].append(new_output)
                    
                    # stream
                    elif output_type == 'stream':
                        name = output.get('name', 'stdout')
                        text = output.get('text', '')
                        if isinstance(text, str):
                            text_list = text.split('\n')
                            while text_list and text_list[-1] == '':
                                text_list.pop()
                            if not text_list:
                                text_list = ['']
                        elif isinstance(text, list):
                            text_list = [str(t) for t in text if t is not None]
                            if not text_list:
                                text_list = ['']
                        else:
                            text_list = ['']
                        
                        new_output = {
                            "output_type": "stream",
                            "name": name,
                            "text": text_list
                        }
                        new_cell['outputs'].append(new_output)
        
        clean_notebook['cells'].append(new_cell)
    
    # 파일 저장
    with open(source_file, 'w', encoding='utf-8') as f:
        json.dump(clean_notebook, f, ensure_ascii=False, indent=1)
    
    print(f"[OK] {source_file} 재생성 완료")
    print(f"[INFO] 셀 개수: {len(clean_notebook['cells'])}")
    
    # 검증
    with open(source_file, 'r', encoding='utf-8') as f:
        verified = json.load(f)
    
    print(f"[OK] JSON 검증 통과")
    
    # 구조 확인
    print(f"[INFO] nbformat: {verified.get('nbformat')}.{verified.get('nbformat_minor')}")
    print(f"[INFO] metadata keys: {list(verified.get('metadata', {}).keys())}")
    print(f"[INFO] 첫 번째 셀 keys: {list(verified['cells'][0].keys()) if verified.get('cells') else []}")

if __name__ == '__main__':
    files = [
        'clustering.ipynb',
        'LinearRegression.ipynb',
        'LOS_Prediction.ipynb',
        'LR_salesPrediction.ipynb',
        'LR_wagePrediction.ipynb'
    ]
    
    for filename in files:
        try:
            create_clean_notebook(filename)
        except Exception as e:
            print(f"{filename} 처리 중 오류: {e}")
            import traceback
            traceback.print_exc()

