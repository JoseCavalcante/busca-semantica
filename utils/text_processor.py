
import re

class RecursiveCharacterTextSplitter:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # Priority of separators: Paragraph -> Sentence -> Words -> Characters
        self.separators = ["\n\n", "\n", ". ", " ", ""]

    def split_text(self, text: str) -> list[str]:
        return self._split_text(text, self.separators)

    def _split_text(self, text: str, separators: list[str]) -> list[str]:
        final_chunks = []
        
        # Get appropriate separator
        separator = separators[-1]
        for s in separators:
            if s == "":
                separator = s
                break
            if s in text:
                separator = s
                break
        
        # Split
        if separator:
            splits = text.split(separator)
        else:
            splits = list(text) # Split by char

        # Merge splits to build chunks
        good_splits = []
        current_chunk = ""
        
        for s in splits:
            if len(current_chunk) + len(s) + len(separator) < self.chunk_size:
                current_chunk += s + separator
            else:
                if current_chunk:
                    good_splits.append(current_chunk.strip())
                
                # If the split itself is too big, recurse
                if len(s) > self.chunk_size and len(separators) > 1:
                     # Find next separator index
                     next_sep_index = separators.index(separator) + 1
                     if next_sep_index < len(separators):
                         sub_chunks = self._split_text(s, separators[next_sep_index:])
                         good_splits.extend(sub_chunks)
                     else:
                         good_splits.append(s[:self.chunk_size]) # Force crop if no more separators
                else:
                    current_chunk = s + separator

        if current_chunk:
             good_splits.append(current_chunk.strip())
             
        return good_splits

# Helper function compatible with legacy calls
def smart_split_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_text(text)
