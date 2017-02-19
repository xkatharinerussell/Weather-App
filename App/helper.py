class helper:
    
    def get_AgeRange(self, age):
        AgeBracket= ["12:14", "15:17", "18:25", "26:35", "36:45", "46:50"]
        if 12<=age<=14:
            return AgeBracket[0]
        elif 15<=age<=17:
            return AgeBracket[1]
        elif 18<=age<=25:
            return AgeBracket[2]
        elif 26<=age<=35:
            return AgeBracket[3]
        elif 36<=age<=45:
            return AgeBracket[4]
        else:
            return AgeBracket[5]
        
    def get_Temp(self, temp):
        TempRange= ["-50:-5", "-4:8", "9:15", "16:20", "21:25", "26:29", "30:34", "35:50"]
        if -50<=temp<=-5:
            return TempRange[0]
        elif -4<=temp<=8:
            return TempRange[1]        
        elif 9<=temp<=15:
            return TempRange[2] 
        elif 16<=temp<=20:
            return TempRange[3] 
        elif 21<=temp<=25:
            return TempRange[4]
        elif 26<=temp<=29:
            return TempRange[5]  
        elif 30<=temp<=34:
            return TempRange[6] 
        else:
            return TempRange[7] 
        
            
        
        
    