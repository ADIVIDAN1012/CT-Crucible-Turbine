import os  
base = os.path.join(os.environ['USERPROFILE'], 'OneDrive', 'Desktop', 'Academic Notes', 'Semester 6', 'Major Project', 'Orbit')  
out = os.path.join(base, 'final_report.tex')  
f = open(out, 'w', encoding='utf-8')  
w = f.write  
print('Setup OK')  
w = f.write  
import os  
base = os.path.join(os.environ.get('USERPROFILE',''), 'OneDrive', 'Desktop', 'Academic Notes', 'Semester 6', 'Major Project', 'Orbit')  
out = os.path.join(base, 'final_report.tex')  
f = open(out, 'a', encoding='utf-8')  
w = f.write  
w(r""" >> gen.py && echo. >> gen.py && echo The proliferation of distributed development methodologies, microservices architectures, and cloud-native deployment strategies has fundamentally transformed how software teams collaborate. In environments where multiple stakeholders contribute to a shared codebase, the principle of least privilege must be strictly enforced to prevent unauthorized access, accidental data corruption, and malicious insider threats. The Project Orbit system addresses this challenge by implementing a novel five-tier role isolation protocol that maps each team member to a dedicated workspace scope with clearly defined access boundaries. >> gen.py && echo """)  
