# define tokenizer for latex expression

# read defined latex tokens
with open('./data/latex_token.txt', 'r') as f:
    latex_token = f.readline().split(';')

# drop the last null token
latex_token = latex_token[:-1]
    
    
class latex_tokenizer:
    SOS = 0 # start of string
    EOS = 1 # end of string
    
    def __init__(self):
        self.n_token = 2
        self.token2index = {'SOS': self.SOS, 'EOS': self.EOS}
        self.index2token = {self.SOS: 'SOS', self.EOS: 'EOS'}
        self.token_count = {} # not counting SOS/EOS
        
        # initialize the two dictionaries
        for token in latex_token:
            self.token2index[token] = self.n_token
            self.index2token[self.n_token] = token
            self.token_count[token] = 0
            self.n_token += 1
            
    
    
    # convert input expression to index representation using the tokenizer
    def tokenize(self, expression):
        '''
        expression: must be a string
        '''
        
        result = [self.token2index['SOS']]
        buffer = ''
        
        for c in expression:
            
            if buffer not in self.token2index:
                buffer += c
            
            # updated buffer: need to check it again
            if buffer in self.token2index:
                result.append(self.token2index[buffer])
                self.token_count[buffer] += 1
                buffer = ''
        
        # if buffer is non-empty, there is error
        if buffer != '':
            return -1
        
        result.append(self.token2index['EOS'])
        return result
    
    
    
    # convert input tokens back to latex expression
    # ignore SOS/EOS
    def detokenize(self, indices):
        '''
        indices: list of indices
        '''
        string = ''
        
        for i in indices:
            token = self.index2token[i]
            if token != 'SOS' and token != 'EOS':
                string = string + token
        
        return string
    
    

# token for natural expression would just be word
class natural_vectorizer:
    SOS = 0 # start of string
    EOS = 1 # end of string
    
    def __init__(self):
        self.n_word = 2
        self.word2index = {'SOS': self.SOS, 'EOS': self.EOS}
        self.index2word = {self.SOS: 'SOS', self.EOS: 'EOS'}
        self.word_count = {} # not counting SOS/EOS
        
        
    
    def vectorize(self, expression):
        result = [self.word2index['SOS']]
        buffer = ''
        
        words = expression.split(' ')
        
        for w in words:
            if w not in self.word2index:
                # add new word
                self.word2index[w] = self.n_word
                self.index2word[self.n_word] = w
                self.word_count[w] = 1
                self.n_word += 1
                
                # append result
                result.append(self.word2index[w])
                
            else:
                self.word_count[w] += 1
                result.append(self.word2index[w])
        
        result.append(self.word2index['EOS'])
        return result
    
    def devectorize(self, vec):
        string = ''
        
        for v in vec:
            word = self.index2word[v]
            if word != 'SOS' and word != 'EOS':
                string = string + word
                
        return string