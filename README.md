# Danawa_VGA_graph

코인과 함께 변동되고 있는 그래픽 카드 가격을 확인하고자 그래프를 생성

# Install

```bash
pip install -r requirements.txt
```

# How to use

포함하고 싶은 단어를 contain_str 에 포함시키지 않을 단어를 without_str로 설정  

ex) 3060 Ti 제외 3060
```bash
python graph.py --contain_str 3060 --without_str Ti
```