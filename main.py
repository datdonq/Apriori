import pandas as pd
from itertools import combinations
# input:
#   TID        items
# 0  T1     I1,I2,I5
# 1  T2        I2,I4
# 2  T3        I2,I3
# 3  T4     I1,I2,I4
# 4  T5        I1,I3
# 5  T6        I2,I3
# 6  T7        I1,I3
# 7  T8  I1,I2,I3,I5
# 8  T9     I1,I2,I3   

# Trả về từng list items của khách hàng
def dataSet(file_name):
    data_set=pd.read_excel(file_name+'.xlsx')
    items =data_set['items'].str.split(",")
    return items
# 0        [I1, I2, I5]
# 1            [I2, I4]
# 2            [I2, I3]
# 3        [I1, I2, I4]
# 4            [I1, I3]
# 5            [I2, I3]
# 6            [I1, I3]
# 7    [I1, I2, I3, I5]
# 8        [I1, I2, I3]

#Trả về số support của mỗi mặt hàng
def count_item(items):
    count_ind_item = {}
    for row in items:
        for i in range(len(row)):
            count_ind_item[row[i]]=count_ind_item.get(row[i],0)+1 
    data = pd.DataFrame()
    data['item_sets'] = count_ind_item.keys()
    data['supp_count'] = count_ind_item.values()
    data = data.sort_values('item_sets')
    return data
#   item_sets  supp_count
# 0        I1           6
# 1        I2           7
# 4        I3           6
# 3        I4           2
# 2        I5           2

# Số support của các item_set
def count_itemset(items, itemsets):
    count_item = {}
    for item_set in itemsets:
        set_A = set(item_set)
        item_set=tuple(item_set)
        for row in items:
            set_B = set(row)
            if set_B.intersection(set_A) == set_A: 
                count_item[item_set]=count_item.get(item_set,0)+1
    data = pd.DataFrame()
    data['item_sets'] = count_item.keys()
    data['supp_count'] = count_item.values()
    return data
# print(count_itemset(items,[['I1','I2'],['I2','I5']]))
#output:
#   item_sets  supp_count
# 0  (I1, I2)           4
# 1  (I2, I5)           2

#Kiểm tra xem item_set có supp lớn hơn min supp hay không 
def check_support(data,supp):
    df = data[data.supp_count >= supp] 
    return df
#Hàm tạo ra các item_set từ tập các items
def join(list_of_items):
    itemsets=[]
    i=1
    for entry in list_of_items:
        proceding_items=list_of_items[i:]
        for item in proceding_items:
            if (type(item) is str):
                if entry!=item:
                    tuples=(entry,item)
                    itemsets.append(tuples)
            else:
                if entry[0:-1] ==item[0:-1]:
                    tuples=entry+item[1:]
                    itemsets.append(set(tuples))
        i+=1
    if len(itemsets)==0:
        return None
    return itemsets
# VD1:
# l=['I1','I2','I3','I4','I5']
# print(join(l))
# Output : [('I1', 'I2'), ('I1', 'I3'), ('I1', 'I4'), ('I1', 'I5'), 
#           ('I2', 'I3'), ('I2', 'I4'), ('I2', 'I5'), ('I3', 'I4'), ('I3', 'I5'), ('I4', 'I5')] 

# VD2:
# s=[('I1','I2'),('I1','I3'),('I1','I5'),('I2','I3'),('I2','I4'),('I2','I5')]
# print(join(s))
# [('I1', 'I2', 'I3'), ('I1', 'I2', 'I5'), ('I1', 'I3', 'I5'), ('I2', 'I3', 'I4'), ('I2', 'I3', 'I5'), ('I2', 'I4', 'I5')]

def apriori(items,supp):
    R=pd.DataFrame()
    df=count_item(items)
    while len(df)!=0:
        df=check_support(df,supp)
        R=pd.concat([R,df])
        itemsets=join(df.item_sets)
        if (itemsets is None):
            return R
        df=count_itemset(items,itemsets)
    return df
#Tính số support của từng tập itemset kiểu frozenset
def find_supp(frozen_set_of_items):
    global items
    count=0
    for i in items:
        if frozen_set_of_items.issubset(i) :
            count+=1
    return count
if __name__=="__main__":
    items=dataSet(input("Enter file_data'names : "))
    min_supp=(int(input("Enter minimum support(%) :"))*len(items))/100
    min_confidence=int(input("Enter minimum confidence(%) :"))
    l=apriori(items,min_supp)
    l=l['item_sets']
    for L in l:
        if type(L) is not str:
            C = [frozenset(item) for item in combinations(L, len(L) - 1)]
            for a in C:
                b = frozenset(L) - a
                set_ab = frozenset(L)
                supp_ab = find_supp(set_ab)
                supp_a = find_supp(a)
                supp_b = find_supp(b)
                confidence_1 = supp_ab / supp_a * 100
                if (confidence_1 >= min_confidence):
                    print(str(list(a)) + ' -> ' + str(list(b)) + ' = ' + str(round(confidence_1)) + '%')
                if len(L)>=3:
                    confidence_2 = supp_ab / supp_b * 100
                    if (confidence_2 >= min_confidence):
                        print(str(list(b)) + ' -> ' + str(list(a)) + ' = ' + str(round(confidence_2)) + '%')
                print()
