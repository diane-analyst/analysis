import json

def fix_notebook_metadata(filename):
    """노트북 파일의 metadata를 올바르게 수정합니다."""
    print(f"\n=== {filename} metadata 수정 중 ===\n")
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 최상위 metadata 확인 및 수정
    if 'metadata' not in data:
        data['metadata'] = {}
    
    metadata = data['metadata']
    
    # kernelspec 확인
    if 'kernelspec' not in metadata:
        metadata['kernelspec'] = {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        }
    else:
        # kernelspec 필수 필드 확인
        if 'display_name' not in metadata['kernelspec']:
            metadata['kernelspec']['display_name'] = "Python 3"
        if 'language' not in metadata['kernelspec']:
            metadata['kernelspec']['language'] = "python"
        if 'name' not in metadata['kernelspec']:
            metadata['kernelspec']['name'] = "python3"
    
    # language_info 확인
    if 'language_info' not in metadata:
        metadata['language_info'] = {
            "name": "python",
            "version": "3.8.0"
        }
    else:
        # language_info 필수 필드 확인
        if 'name' not in metadata['language_info']:
            metadata['language_info']['name'] = "python"
        if 'version' not in metadata['language_info']:
            metadata['language_info']['version'] = "3.8.0"
    
    # 각 셀의 metadata 확인
    for i, cell in enumerate(data.get('cells', [])):
        if 'metadata' not in cell:
            cell['metadata'] = {}
        elif not isinstance(cell['metadata'], dict):
            cell['metadata'] = {}
    
    # nbformat 버전 확인
    if 'nbformat' not in data:
        data['nbformat'] = 4
    if 'nbformat_minor' not in data:
        data['nbformat_minor'] = 4
    
    # 파일 저장
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    
    print(f"[OK] {filename} metadata 수정 완료")
    
    # 검증
    with open(filename, 'r', encoding='utf-8') as f:
        verified = json.load(f)
    
    print(f"[OK] JSON 검증 통과")
    print(f"[INFO] 최상위 metadata 키: {list(verified.get('metadata', {}).keys())}")
    print(f"[INFO] kernelspec: {verified.get('metadata', {}).get('kernelspec', {})}")
    print(f"[INFO] language_info: {verified.get('metadata', {}).get('language_info', {})}")

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
            fix_notebook_metadata(filename)
        except Exception as e:
            print(f"{filename} 처리 중 오류: {e}")
            import traceback
            traceback.print_exc()

