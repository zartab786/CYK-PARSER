import nltk
from nltk.tokenize import sent_tokenize
import re
import string
from Back import back
from nltk import Tree
#Loading the grammar
grammar=nltk.data.load("grammars/large_grammars/atis.cfg")
#grammar=nltk.data.load("grammars/sample_grammars/toy.cfg")
#print(grammar)
grammar=grammar.chomsky_normal_form(new_token_padding='@$@', flexible=False)
#print(dir(grammar))
def move_back(value):
		if value.child1==None and value.child2==None:
			return str(value.root)+" "+str(value.ending)

		#value1=move_back(value.child1)
		#value2=move_back(value.child2)
		#print(value)

		return "("+str(value.root)+"("+str(move_back(value.child1))+")"+" "+"("+str(move_back(value.child2))+")"+")"
"""for production in grammar._productions:
	if( str(production._lhs)=="NREL_BER@$@NP_DT"):
		print(production)

	if(str(production._lhs)=="SIGMA" and "pt_verb_ber" in str(production._rhs)):
		print(production)"""


#loading the raw sentences of the test set of grammar

dict_grammar={}

for production in grammar._productions:
	prod=production._rhs
	if(len(prod)==1):
		prod=str(prod[0])
		dict_grammar[prod]=[]
	else:
		prod=str(prod[0])+ " "+str(prod[1])
		dict_grammar[prod]=[]

for production in grammar._productions:
	prod=production._rhs
	if(len(prod)==1):
		prod=str(prod[0])
		dict_grammar[prod].append(production._lhs)
	else:
		prod=str(prod[0])+ " "+str(prod[1])
		dict_grammar[prod].append(production._lhs)


s = str(nltk.data.load("grammars/large_grammars/atis_sentences.txt", "raw"))

#print(len(dict_grammar))
#print(s)

#cleaning the test sentences of the grammar for to use in our own built CYK parser
s=re.sub(r"\\n","",s)
s=re.sub(r"\d+","",s)
#print(s)

list_of_sentences=s.split(":")
list_of_sentences=list_of_sentences[3:]
list_of_sentences=[s.strip() for s in list_of_sentences]
#print(list_of_sentences)
#print(len(list_of_sentences))
#list_of_sentences=["i want to book my flight .".split()]


"""for production in grammar._productions:
	lhs=production._lhs
	if(lhs in dict_non_terminal.keys()):
		dict_non_terminal[lhs]=dict_non_terminal[lhs] +1
	else:
		dict_non_terminal[lhs]=1	"""



parser = nltk.ChartParser(grammar) # parse all test sentences

	


for sentence in list_of_sentences:


	#print(tokens)
	parse_trees=set()
	#tokens2="i need a flight from charlotte to las vegas that makes a stop in saint louis ."
	tokens2=sentence.split()
	tokens=["","what","are","the","costs","."]
	#tokens=[""]
	"""for i in range(0,len(tokens2)):
		tokens.append(tokens2[i])"""

	#print(tokens)	
	list_2d=[[set() for col in range(len(tokens)+1)]for row in range(len(tokens)+1)]
	backpointer=[[[] for col in range(len(tokens)+1)] for row in range(len(tokens)+1)]
	count=0
	for i in range(1,len(tokens)):
		if(tokens[i] in dict_grammar.keys()):
			prod=dict_grammar[tokens[i]]

			for lhs in prod:

				list_2d[i][i].add(lhs)
				backpointer[i][i].append(back(None,None,lhs,tokens[i]))
					#print(i,i)
				#print(backpointer[i][i])
				#count+=1
	#print(list_2d)
	#print(backpointer)
	#print(count)


	for i in range(2,len(tokens)):
		for j in range(1,len(tokens)-i+1):
	# 		dict_back={}
			for k in range(j,j+i-1):
				#list_2d[j][j+i-1]= union of list_2d[j][k] + union of list_2d[k+1][j+i-1]
				
				for p in list_2d[j][k]:
					for q in list_2d[k+1][j+i-1]:
						#term=str(p) + "@$@" + str(q)
						term2=str(p) + " " + str(q)
						#print(j,j+i-1)

						if(len(term2.split())==2 and term2 in dict_grammar.keys()):
							prod=dict_grammar[term2]

							for lhs in prod:
								list_2d[j][j+i-1].add(lhs)

								prod1=term2.split()
									#print(j,j+i-1)

									
								for point1 in backpointer[j][k]:
									#print(j,k)
									#print(j,j+i-1)
									#print(backpointer[j][j+i-1])

									for point2 in backpointer[k+1][j+i-1]:
										#print(j,k)
										#print(point1.root,point2.root)
										#print(j,j+i-1)
										#print(term2)
										if(str(point1.root)==prod1[0] and str(point2.root)==prod1[1]):
											
											backpointer[j][j+i-1].append(back(point1,point2,lhs,None))


		
	#print(list_2d[1][len(tokens)-1])
	#print(backpointer)
	#print(list_2d)

	


	if("SIGMA" in str((list_2d[1][len(tokens)-1]))):
		print("YES")
		for point in backpointer[1][len(tokens)-1]:
			#print(point.root)
			if(str(point.root)=="SIGMA"):
				#count=0
				result=move_back(point)
				#print(result)
				parse_trees.add(result)
				
				

		
		print(parse_trees)
		print(len(parse_trees))	
		for result in parse_trees:
			trees=Tree.fromstring(result)
			trees.draw()
				
				

	else:
		print("NO")


	# #print(list_2d[1][len(tokens)-1])
	

	# #print(list_2d)
	# """for i in range(1,len(tokens)):
	# 	for j in range(1,len(tokens)):
	# 		print(i,j)

	# 		print(list_2d[i][j])"""

	break
		
	




		

	







