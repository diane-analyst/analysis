import json
import sys

def validate_and_fix_notebook(filename):
    """노트북 파일을 nbformat v5.10.4 스펙에 맞게 검증하고 수정합니다."""
    print(f"\n=== {filename} 검증 및 수정 ===\n")
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    issues = []
    
    # 1. 최상위 레벨 필수 필드 확인
    required_top = ['cells', 'metadata', 'nbformat', 'nbformat_minor']
    for key in required_top:
        if key not in data:
            issues.append(f"최상위 레벨에 '{key}' 필드 누락")
            if key == 'cells':
                data['cells'] = []
            elif key == 'metadata':
                data['metadata'] = {}
            elif key == 'nbformat':
                data['nbformat'] = 4
            elif key == 'nbformat_minor':
                data['nbformat_minor'] = 4
    
    # 2. metadata 구조 확인
    if 'metadata' not in data:
        data['metadata'] = {}
    
    metadata = data['metadata']
    
    # kernelspec 필수
    if 'kernelspec' not in metadata:
        metadata['kernelspec'] = {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        }
        issues.append("metadata에 'kernelspec' 추가됨")
    
    # language_info 필수
    if 'language_info' not in metadata:
        metadata['language_info'] = {
            "name": "python",
            "version": "3.8.0"
        }
        issues.append("metadata에 'language_info' 추가됨")
    
    # 3. 각 셀의 metadata 확인
    for i, cell in enumerate(data.get('cells', [])):
        if 'metadata' not in cell:
            cell['metadata'] = {}
            issues.append(f"셀 {i}에 'metadata' 추가됨")
        elif not isinstance(cell['metadata'], dict):
            cell['metadata'] = {}
            issues.append(f"셀 {i}의 'metadata' 타입 수정됨")
        
        # cell_type 필수
        if 'cell_type' not in cell:
            issues.append(f"셀 {i}에 'cell_type' 누락")
        
        # source 필수
        if 'source' not in cell:
            cell['source'] = ['']
            issues.append(f"셀 {i}에 'source' 추가됨")
        elif not isinstance(cell['source'], list):
            cell['source'] = [str(cell['source'])]
            issues.append(f"셀 {i}의 'source' 타입 수정됨")
        
        # 코드 셀의 경우
        if cell.get('cell_type') == 'code':
            if 'execution_count' not in cell:
                cell['execution_count'] = None
            if 'outputs' not in cell:
                cell['outputs'] = []
            elif not isinstance(cell['outputs'], list):
                cell['outputs'] = []
    
    if issues:
        print(f"발견된 문제 및 수정 사항 ({len(issues)}개):")
        for issue in issues[:10]:
            print(f"  - {issue}")
        if len(issues) > 10:
            print(f"  ... 및 {len(issues) - 10}개 더")
    else:
        print("[OK] 문제 없음")
    
    # 파일 저장
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    
    print(f"\n[OK] {filename} 수정 완료")
    
    # 최종 검증
    with open(filename, 'r', encoding='utf-8') as f:
        verified = json.load(f)
    
    print(f"[OK] JSON 검증 통과")
    print(f"[INFO] nbformat: {verified.get('nbformat')}.{verified.get('nbformat_minor')}")
    print(f"[INFO] 셀 개수: {len(verified.get('cells', []))}")
    
    return len(issues) == 0

if __name__ == '__main__':
    files = [
        'clustering.ipynb',
        'LinearRegression.ipynb',
        'LOS_Prediction.ipynb',
        'LR_salesPrediction.ipynb',
        'LR_wagePrediction.ipynb'
    ]
    
    all_ok = True
    for filename in files:
        try:
            if not validate_and_fix_notebook(filename):
                all_ok = False
        except Exception as e:
            print(f"{filename} 처리 중 오류: {e}")
            import traceback
            traceback.print_exc()
            all_ok = False
    
    if all_ok:
        print("\n[OK] 모든 파일 검증 통과!")
    else:
        print("\n[WARNING] 일부 파일에 문제가 있었지만 수정되었습니다.")

