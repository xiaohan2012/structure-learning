all: chowliu gpt concat

chowliu: chowliu_result
	cp p1/*.txt ~/public_html/pmp/

chowliu_result:
	python chow_liu_tree.py predict > result/chowliu_probs.txt
	python chow_liu_tree.py sorted_edges > result/chowliu_arcs.txt
	python chow_liu_tree.py graph_viz > result/chowliu.dot

gpt:  concat3
	chmod a+r ~/public_html/pmp/*
	cp p3/*.txt ~/public_html/pmp/

gpt_orig:
	python gpt.py orig predict > result/gpt_orig_probs.txt
	python gpt.py orig sorted_edges > result/gpt_orig_arcs.txt
	python gpt.py orig graphviz > result/gpt_orig.dot

gpt_mod:
	python gpt.py mod predict > result/gpt_mod_probs.txt
	python gpt.py mod sorted_edges > result/gpt_mod_arcs.txt
	python gpt.py mod graphviz > result/gpt_mod.dot

concat3: 
#rm p3/HanXiao_3_probs.txt p3/HanXiao_3_arcs.txt
	cat result/chowliu_probs.txt  >> p3/HanXiao_3_probs.txt
	echo "--------------------------Using Chow-Liu tree algorithm-----------------------------"  >> p3/HanXiao_3_probs.txt
	cat result/gpt_orig_probs.txt  >> p3/HanXiao_3_probs.txt
	echo "--------------------------Using original GPT tree algorithm-----------------------------"  >> p3/HanXiao_3_probs.txt
	cat result/gpt_mod_probs.txt  >> p3/HanXiao_3_probs.txt
	echo "--------------------------Using modified GPT tree algorithm-----------------------------"  >> p3/HanXiao_3_probs.txt
	cat result/chowliu_arcs.txt  >> p3/HanXiao_3_arcs.txt
	echo "--------------------------Using Chow-Liu tree algorithm-----------------------------"  >> p3/HanXiao_3_arcs.txt
	cat result/gpt_orig_arcs.txt  >> p3/HanXiao_3_arcs.txt
	echo "--------------------------Using original GPT tree algorithm-----------------------------"  >> p3/HanXiao_3_arcs.txt
	cat result/gpt_mod_arcs.txt  >> p3/HanXiao_3_arcs.txt
	echo "--------------------------Using modified GPT tree algorithm-----------------------------"  >> p3/HanXiao_3_arcs.txt
