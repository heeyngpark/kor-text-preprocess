from .utils import Refine
from tqdm import tqdm

class Template(Refine):
    def __init__(self, task):
        super().__init__()
        if task == 'next_sentence_prediction':
            self.task = self.next_sentence_prediction
        else:
            print("{} is not available}".format(task))
            raise ValueError
    
    def apply(self, *args, **kwargs):
        self.task(*args, **kwargs)

    def next_sentence_prediction(self, inp_path, out_path, \
                                min_seq=0, sep='다.', encoding='utf8'):
        """
        Read lines from input file and split sentences by [SEP]
        ex1) In:"A[SEP]B[SEP]C[SEP]D[SEP]\n" -> Out:"A[SEP]\tB[SEP]\nC[SEP]\tD[SEP]\n" 
        ex2) In:"A[SEP]B[SEP]C[SEP]\n D[SEP]E[SEP]\n" -> \
             Out:"A[SEP]\tB[SEP]\nC[SEP]\tD[SEP]\n"
        """

        num_lines = sum(1 for line in open(inp_path, "r", encoding=encoding))
        lines = super().readline(inp_path, encoding)
        with open(out_path, "w", encoding=encoding) as out:
            remainder = []
            for line in tqdm(lines, total=num_lines):
                if not line:
                    break
                start = 0
                while True:
                    end = line.find(sep, start)
                    if end == -1:
                        break
                    if end-start >= min_seq:
                        remainder.append(line[start:end+len(sep)])
                    start = end + len(sep)
                for i in range(len(remainder)-1):
                    if i % 2 == 0:
                        sen1 = remainder.pop(0)
                        sen2 = remainder.pop(0)
                        out.write(sen1 + "\t" + sen2 + "\n")
        print("process done, saved at {}".format(out_path))
             