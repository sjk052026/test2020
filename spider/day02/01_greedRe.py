import re

html = """
<div><p>如果你为门中弟子伤他一份,我便屠你满门</p></div>
<div><p>如果你为天下人损他一毫,我便杀净天下人</p></div>
"""

pattern = re.compile('<div><p>(.*?)</p></div>', re.S)
r_list=pattern.findall(html)
print(r_list)