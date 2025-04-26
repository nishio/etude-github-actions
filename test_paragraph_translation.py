import unittest
from translate_page_based import (
    preprocess_scrapbox_notation, 
    postprocess_scrapbox_notation, 
    group_lines_into_paragraphs,
)


def generate_test_line(text):
    return {
        "text": text,
        "created": 946652400,
        "updated": 946652400,
        "userId": "582e63d27c56960011aff09e",
    }


class TestParagraphTranslation(unittest.TestCase):
    
    def test_preprocess_scrapbox_notation(self):
        input_text = "これは[リンク]のテストです。[複数][リンク]も処理します。"
        expected = "これは__SCRAPBOX_LINK_START__リンク__SCRAPBOX_LINK_END__のテストです。__SCRAPBOX_LINK_START__複数__SCRAPBOX_LINK_END____SCRAPBOX_LINK_START__リンク__SCRAPBOX_LINK_END__も処理します。"
        self.assertEqual(preprocess_scrapbox_notation(input_text), expected)
    
    def test_postprocess_scrapbox_notation(self):
        input_text = "これは__SCRAPBOX_LINK_START__リンク__SCRAPBOX_LINK_END__のテストです。"
        expected = "これは[リンク]のテストです。"
        self.assertEqual(postprocess_scrapbox_notation(input_text), expected)
    
    def test_group_lines_into_paragraphs(self):
        lines = [
            generate_test_line("Line 1"),
            generate_test_line("Line 2"),
            generate_test_line(""),
            generate_test_line(" Indented line 1"),
            generate_test_line(" Indented line 2"),
            generate_test_line("  Double indented"),
            generate_test_line("[en.icon] Test"),
        ]
        
        paragraphs = group_lines_into_paragraphs(lines)
        
        self.assertEqual(len(paragraphs), 5)
        
        self.assertEqual(len(paragraphs[0]), 2)
        self.assertEqual(paragraphs[0][0]["text"], "Line 1")
        self.assertEqual(paragraphs[0][1]["text"], "Line 2")
        
        self.assertEqual(len(paragraphs[1]), 1)
        self.assertEqual(paragraphs[1][0]["text"], "")
        
        self.assertEqual(len(paragraphs[2]), 2)
        self.assertEqual(paragraphs[2][0]["text"], " Indented line 1")
        self.assertEqual(paragraphs[2][1]["text"], " Indented line 2")
        
        self.assertEqual(len(paragraphs[3]), 1)
        self.assertEqual(paragraphs[3][0]["text"], "  Double indented")
        
        self.assertEqual(len(paragraphs[4]), 1)
        self.assertEqual(paragraphs[4][0]["text"], "[en.icon] Test")


if __name__ == "__main__":
    unittest.main()
