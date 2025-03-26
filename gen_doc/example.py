import re

filename = [
    "mikroqarz_78_xulosa",
    "mikroqarz_78_xulosa_qr1",
    "mikroqarz_78_xulosa_qr2",
    "mikroqarz_78_xulosa_qr3",
    "mikroqarz_78_xulosa_qr4"
]

# Fayl nomidan _qr va raqamlarni olib tashlaymiz
clean_filenames = [re.sub(r"_qr\d+$", "", filename) for filename in filenames]

print(clean_filenames[0])
