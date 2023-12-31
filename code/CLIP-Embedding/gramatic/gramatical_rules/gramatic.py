class Gramatic:
    '''
    `!TOKEN` indica que compara que sea distinto de TOKEN
    '''
    use_preference = True #si ya se esta usando un token como token de posicion entonces no usar otros tokens con relacion a este ditinto de la relacion original, ergo segun el orden de las `relation`, si hay ambiguedad usa el primero, puede quedar ambiguo igual, pero menos

    def __init__(self, relation = None) -> None:
        self.result = []
        self.relation = relation
    
    def pos_case(self, sentence, text, i, j, temp):
        result  = [value for value in temp]
        if text[i] != "POS" and text[i] != "POSITION":
            return False

        while text[i] == "POS" or text[i] == "POSITION":
            result+=[i]
            i+=1
        return i,j,result
        
    def text_case(self,sentence, text, i, j, temp):
        #caso especial que hay que tratar
        j+=1
        break_next = False
        while i<len(text):
            i+=1
            if i>=len(text): break

            if break_next:
                i -= 1
                return (True,i)
            
            if text[i] == '.' or text[i] =='|':
                break_next = True


            temp_i = i
            temp_j = j
            temp_temp = [value for value in temp]

            while (text[i] == sentence[j] or (sentence[j] == 'text' and text[i]=='WORD'))\
                or (sentence[j][0] == '!' and sentence[j][1:] != text[i]) \
                or sentence[j] == 'pos' and self.pos_case(sentence,text,i,j,temp) != False:
                
                if sentence [j] == 'pos':
                    i,j,temp = self.pos_case(sentence,text,i,j,temp)

                    if j == len(sentence)-1:
                        return (i,j,temp)
                    j+=1
                    continue
                
                if sentence[j] == 'text' and len(sentence) > j+1:
                    text_analiced = self.text_case(sentence,text,i,j,temp)
                    if text_analiced == False:
                        break
                    elif text_analiced[0] == True:
                        i = text_analiced[1]
                        break
                    else:    
                        i,j,temp = text_analiced

                        if j == len(sentence)-1:
                            return (i,j,temp)
                        continue

                if text[i] != 'WORD':
                    temp +=[i]
                
                if j == len(sentence)-1:
                    return (i,j,temp)
                i+=1
                j+=1
                
            #Si llega a aqui no matcheo. Luego hay que buscar otro x donde comience a matchaer
            i = temp_i
            j = temp_j
            temp = temp_temp

        return False    
    
    def match(self,sentence, text):
        result = []
        i= -1

        while i < len(text)-1:
            i+=1
            temp = []
            j= -1
            while j < len(sentence)-1:
                j+=1
                if sentence[j] == 'text' and len(sentence) > j+1:
                    text_analiced = self.text_case(sentence,text,i,j,temp)
                    if text_analiced == False:
                        return result
                    elif text_analiced[0] == True:
                        i = text_analiced[1]
                        break
                    else:    
                        i,j,temp = text_analiced
                        is_temp_used = self.is_temp_used(temp,text)
                        # is_temp_used = True in [ self.result[index] for index in temp] 
                        if not self.use_preference or not is_temp_used:
                            result += temp
                        break

                if sentence[j] =='pos':        
                    pos_analiced = self.pos_case(sentence,text,i,j,temp)
                    if pos_analiced == False:
                        break
                    i,j,temp = pos_analiced
                    if j == len(sentence)-1:
                        is_temp_used = self.is_temp_used(temp,text)
                        # is_temp_used = True in [ self.result[index] for index in temp] 
                        if not self.use_preference or not is_temp_used:
                            result += temp
                            break
                    continue    

                if text[i] == sentence[j] or (sentence[j][0] == '!' and sentence[j][1:] != text[i]):
                    if text[i] != 'WORD':
                        temp += [i]
                    i+=1
                else:
                    break
                if j == len(sentence)-1:
                    is_temp_used = self.is_temp_used(temp,text)
                    # is_temp_used = True in [ self.result[index] for index in temp] 
                    if not self.use_preference or not is_temp_used:
                        result += temp
        return result

    def is_temp_used(self,temp,text):
        useds = [ self.result[index] for index in temp]
        if len(useds) >=3:
            is_used = True in useds[1:-1]
            if not is_used:
                is_used = (self.result[temp[0]] and text[temp[0]] != ',') or (self.result[temp[-1]] and text[temp[-1]] != ',') 
        else:
            is_used = True in useds
        return is_used    

    def get_tokens(self, text):
        self.result = [False]*len(text)
        for sentence in self.relation:
            indexs = self.match(sentence.split(" "),text)
            for index in indexs:
                self.result[index] = True
        return self.result