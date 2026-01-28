# Embedding Model Performance Report
- Date: 2026-01-28 17:48:23
- Ethos Server: http://192.168.40.54:11435

Fetching tags from http://192.168.40.54:11435...
Found 3 models: bge-m3:latest, mxbai-embed-large:latest, nomic-embed-text:latest

============================================================
 TESTING MODEL: bge-m3:latest
============================================================
 - Generated for: '안녕하세요, 저는 백엔드 개...' | Dim: 1024 | Time: 0.3024s
 - Generated for: 'Spring Boot와 JP...' | Dim: 1024 | Time: 0.1371s
 - Generated for: 'Hello, I am a b...' | Dim: 1024 | Time: 0.1333s
 - Generated for: 'I have experien...' | Dim: 1024 | Time: 0.1316s

[Performance] Total: 0.7085s | Avg: 0.1771s per request
[Similarity] KR-EN Cross: 0.9195
[Similarity] Related (KR): 0.4838

============================================================
 TESTING MODEL: mxbai-embed-large:latest
============================================================
 - Generated for: '안녕하세요, 저는 백엔드 개...' | Dim: 1024 | Time: 0.0338s
 - Generated for: 'Spring Boot와 JP...' | Dim: 1024 | Time: 0.0394s
 - Generated for: 'Hello, I am a b...' | Dim: 1024 | Time: 0.0387s
 - Generated for: 'I have experien...' | Dim: 1024 | Time: 0.0405s

[Performance] Total: 0.1556s | Avg: 0.0389s per request
[Similarity] KR-EN Cross: 0.4510
[Similarity] Related (KR): 0.6260

============================================================
 TESTING MODEL: nomic-embed-text:latest
============================================================
 - Generated for: '안녕하세요, 저는 백엔드 개...' | Dim: 768 | Time: 0.0259s
 - Generated for: 'Spring Boot와 JP...' | Dim: 768 | Time: 0.0275s
 - Generated for: 'Hello, I am a b...' | Dim: 768 | Time: 0.0272s
 - Generated for: 'I have experien...' | Dim: 768 | Time: 0.0278s

[Performance] Total: 0.1111s | Avg: 0.0278s per request
[Similarity] KR-EN Cross: 0.6303
[Similarity] Related (KR): 0.9219


############################################################
 FINAL COMPARISON SUMMARY (Sorted by Speed)
############################################################
Model Name                     | Dim   | Avg Time   | KR-EN Sim 
-----------------------------------------------------------------
nomic-embed-text:latest        | 768   |   0.0278s |     0.6303
mxbai-embed-large:latest       | 1024  |   0.0389s |     0.4510
bge-m3:latest                  | 1024  |   0.1771s |     0.9195
############################################################

Report saved to: c:\big20\final\report\embedding_test_result_260128_1748.md
