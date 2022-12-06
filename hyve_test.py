import sys

USE_TRIVIAL_IMPLEMENTATION = 0

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class sequence:
    err_code = 63

    def __init__(self):
        pass

    def read(self):
        self.input_value = input("Enter a value in hex notation ex: 00 3D 01 01 00 3E: ")
        # print(self.input_value)
        # self.input_value = "af aa"
        self.bytes_list = bytearray.fromhex(self.input_value)
        self.ints_sequence = []


        for idx in range(len(self.bytes_list)):
            self.ints_sequence.append(int(self.bytes_list[idx]))
        
        # self.ints_sequence = [0,61, 1,1, 0,62, 3,2, 3,3]

    def is_correct(self, p, q, printed_bytes):
        if printed_bytes == 0 and p !=0 :
            return False

        if p > 0:
            if printed_bytes >= p and q <= p:
                return True
            else:
                return False
        elif p == 0:        
            return True

    def start_end_calc(self, p, q, printed_bytes):
        start = printed_bytes - p
        end = start + q
        return start, end

    def p_q_calc(self, start, end, printed_bytes):
        p = printed_bytes - start
        q = end - start 
        return p, q

    def decode(self):
        self.result = []
        for idx in range(0, (len(self.ints_sequence) - 1), 2):
            p = self.ints_sequence[idx]
            q = self.ints_sequence[idx + 1]            
            
            if self.is_correct(p, q, len(self.result)):
                if p == 0:
                    self.result.append(q)
                elif p >= 0:
                    start, end = self.start_end_calc(p, q, len(self.result))
                    self.result[start:end]
                    self.result.extend(self.result[start:end])
            else:
                self.result.append(self.err_code)

        return(self.result)

    def res_to_hex(self, res):
        if len(res) >0:
            lst = []
            for number in res:
                lst.append(hex(number))
        return ' '.join(lst)

    def trivial_encoding(self):
        if len(self.result) >0:
            self.trivial_encoding_result = []
            for byte in self.result:
                self.trivial_encoding_result.append(0)
                self.trivial_encoding_result.append(byte)
            self.eprint(f"{bcolors.FAIL}Trivial encoding: {bcolors.ENDC} {self.res_to_hex(self.trivial_encoding_result)}")


    def non_trivial_encoding(self):
        if len(self.result) >0:
            self.non_trivial_encoding_result = []
            idx = 0
            while idx < len(self.result):
                byte = self.result[idx]
            # for idx, byte in enumerate(self.result):
                if idx == 0:
                    self.non_trivial_encoding_result.append(0)
                    self.non_trivial_encoding_result.append(byte)
                    idx = idx + 1
                else:
                    indices = [idx]
                    seq_a, seq_b = tuple([(self.result+[''])[slice(ix,iy)] for ix, iy in zip([0]+indices, indices+[-1])])
                    # print(seq_a)
                    # print("****")
                    flag = 0
                    for i in range(len(seq_b)):
                        part_b = seq_b[:len(seq_b)-i]
                        # print(part_b)
                        s = self.KMPSearch(part_b, seq_a)
                        if s is not None: 
                            p,q = self.p_q_calc(s, s+len(part_b), len(seq_a))
                            # print(p,q)
                            self.non_trivial_encoding_result.append(p)
                            self.non_trivial_encoding_result.append(q)
                            flag = 1
                            idx = idx + len(part_b)
                            break
                    if flag == 0:
                        self.non_trivial_encoding_result.append(0)
                        self.non_trivial_encoding_result.append(byte)
                        idx = idx + 1
                    # print(idx)
                

        self.eprint(f"{bcolors.FAIL}Non Trivial encoding: {bcolors.ENDC} {self.res_to_hex(self.non_trivial_encoding_result)}")

    def KMPSearch(self, pat, txt): 
        M = len(pat) 
        N = len(txt) 

        # create lps[] that will hold the longest prefix suffix  
        # values for pattern 
        lps = [0]*M 
        j = 0 # index for pat[] 

        # Preprocess the pattern (calculate lps[] array) 
        self.computeLPSArray(pat, M, lps) 

        i = 0 # index for txt[] 
        while i < N: 
            if pat[j] == txt[i]: 
                i += 1
                j += 1

            if j == M: 
                # print("Found pattern at index " + str(i-j))
                return i-j
                j = lps[j-1] 

            # mismatch after j matches 
            elif i < N and pat[j] != txt[i]: 
                # Do not match lps[0..lps[j-1]] characters, 
                # they will match anyway 
                if j != 0: 
                    j = lps[j-1] 
                else: 
                    i += 1

    def computeLPSArray(self, pat, M, lps): 
        len = 0 # length of the previous longest prefix suffix 

        lps[0] # lps[0] is always 0 
        i = 1

        # the loop calculates lps[i] for i = 1 to M-1 
        while i < M: 
            if pat[i]== pat[len]: 
                len += 1
                lps[i] = len
                i += 1
            else: 
                # This is tricky. Consider the example. 
                # AAACAAAA and i = 7. The idea is similar  
                # to search step. 
                if len != 0: 
                    len = lps[len-1] 

                    # Also, note that we do not increment i here 
                else: 
                    lps[i] = 0
                    i += 1

 


    def eprint(self, *args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    def get_bytes(self, prompt):
        hexes = input(prompt).split()
        return ''.join(chr(int(h,16)) for h in hexes)




if __name__ == '__main__':
    input_seq = sequence()
    input_seq.read ()

    
    print(f"Decoded sequence: {input_seq.res_to_hex(input_seq.decode())}")

    if USE_TRIVIAL_IMPLEMENTATION:
        input_seq.non_trivial_encoding()
    else:
        input_seq.trivial_encoding()



  
   