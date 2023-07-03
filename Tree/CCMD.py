#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re

from ArticutAPI import Articut
articut = Articut()

#描述各種節點的 C-Command 關係 (以下先列出幾種)
CCMDPatDICT = {"ACTION_verb":re.compile("<ACTION_verb>[^<]+</ACTION_verb>(.+<FUNC_inner>的</FUNC_inner>(<MODIFIER>[^<]+</MODIFIER>)?)?(<ENTITY_noun>[^<]+?</ENTITY_noun>|<ENTITY_pronoun>[^<]+?</ENTITY_pronoun>|<ENTITY_person>[^<]+?</ENTITY_person>)"),
               "VerbP":re.compile("<VerbP>[^<]+</VerbP>(.+<FUNC_inner>的</FUNC_inner>(<MODIFIER>[^<]+</MODIFIER>)?)?(<ENTITY_noun>[^<]+?</ENTITY_noun>|<ENTITY_pronoun>[^<]+?</ENTITY_pronoun>|<ENTITY_person>[^<]+?</ENTITY_person>)"),
               "FUNC_negation":re.compile("<FUNC_negation>[^<]+</FUNC_negation>(.+)?<ACTION_verb>[^<]+?</ACTION_verb>(.+<FUNC_inner>的</FUNC_inner>(<MODIFIER>[^<]+</MODIFIER>)?)?(<ENTITY_noun>[^<]+?</ENTITY_noun>|<ENTITY_pronoun>[^<]+?</ENTITY_pronoun>|<ENTITY_person>[^<]+?</ENTITY_person>)"),
               "QUANTIFIER":re.compile("<QUANTIFIER>[^<]+</QUANTIFIER>(.+<FUNC_inner>的</FUNC_inner>(<MODIFIER>[^<]+</MODIFIER>)?)?(<ENTITY_noun>[^<]+?</ENTITY_noun>|<ENTITY_pronoun>[^<]+?</ENTITY_pronoun>|<ENTITY_person>[^<]+?</ENTITY_person>)"),
               "ENTITY_noun":re.compile("(.+<FUNC_inner>的</FUNC_inner>)?<ENTITY_noun>[^<]+</ENTITY_noun>(<VerbP>[^<]+?</VerbP>|<ACTION_verb>[^<]+?</ACTION_verb>|<FUNC_inner>的</FUNC_inner>)((?<!的<FUNC_inner>)<ENTITY_noun>[^<]+?</ENTITY_noun>|<ENTITY_pronoun>[^<]+?</ENTITY_pronoun>|<ENTITY_person>[^<]+?</ENTITY_person>)((<VerbP>[^<]+?</VerbP>|<ACTION_verb>[^<]+?</ACTION_verb>|<FUNC_inner>的</FUNC_inner>)(<ENTITY_noun>[^<]+?</ENTITY_noun>|<ENTITY_pronoun>[^<]+?</ENTITY_pronoun>|<ENTITY_person>[^<]+?</ENTITY_person>))?"),
               "ENTITY_pronoun":re.compile("(.+<FUNC_inner>的</FUNC_inner>)?<ENTITY_pronoun>[^<]+</ENTITY_pronoun>(<VerbP>[^<]+?</VerbP>|<ACTION_verb>[^<]+?</ACTION_verb>)((?<!的<FUNC_inner>)<ENTITY_noun>[^<]+?</ENTITY_noun>|<ENTITY_pronoun>[^<]+?</ENTITY_pronoun>|<ENTITY_person>[^<]+?</ENTITY_person>)((<VerbP>[^<]+?</VerbP>|<ACTION_verb>[^<]+?</ACTION_verb>|<FUNC_inner>的</FUNC_inner>)(<ENTITY_noun>[^<]+?</ENTITY_noun>|<ENTITY_pronoun>[^<]+?</ENTITY_pronoun>|<ENTITY_person>[^<]+?</ENTITY_person>))?"),
               "ENTITY_person":re.compile("(.+<FUNC_inner>的</FUNC_inner>)?<ENTITY_person>[^<]+</ENTITY_person>(<VerbP>[^<]+?</VerbP>|<ACTION_verb>[^<]+?</ACTION_verb>)((?<!的<FUNC_inner>)<ENTITY_noun>[^<]+?</ENTITY_noun>|<ENTITY_pronoun>[^<]+?</ENTITY_pronoun>|<ENTITY_person>[^<]+?</ENTITY_person>)((<VerbP>[^<]+?</VerbP>|<ACTION_verb>[^<]+?</ACTION_verb>|<FUNC_inner>的</FUNC_inner>)(<ENTITY_noun>[^<]+?</ENTITY_noun>|<ENTITY_pronoun>[^<]+?</ENTITY_pronoun>|<ENTITY_person>[^<]+?</ENTITY_person>))?")
              }

def CCMDchecker(inputSTR, argX, argY):
    """
    checking if argX c-command argY
    """
    resultBOOL = False
    inputTagSTR = articut.parse(inputSTR)["result_pos"][0].replace("ENTITY_oov", "ENTITY_noun").replace("ENTITY_nouny", "ENTITY_noun").replace("ENTITY_nounHead", "ENTITY_noun")
    argXTagSTR = articut.parse(argX)["result_pos"][0].replace("ENTITY_oov", "ENTITY_noun").replace("ENTITY_nouny", "ENTITY_noun").replace("ENTITY_nounHead", "ENTITY_noun")
    argYTagSTR = articut.parse(argY)["result_pos"][0].replace("ENTITY_oov", "ENTITY_noun").replace("ENTITY_nouny", "ENTITY_noun").replace("ENTITY_nounHead", "ENTITY_noun")

    if argXTagSTR in inputTagSTR:
        pass
    else:
        return resultBOOL
    if argYTagSTR in inputTagSTR:
        pass
    else:
        return resultBOOL

    argXPOSLIST = [p.group(0) for p in re.finditer("(?<=</)[^<]+(?=>)", argXTagSTR)]
    if len(argXPOSLIST) == 1:
        argXPOS = argXPOSLIST[0]
    elif len(argXPOSLIST) > 1:
        argXPOS = argXPOSLIST[-1]

    if argXPOS in CCMDPatDICT.keys():
        checkingTagLIST =[p.group(0) for p in  CCMDPatDICT[argXPOS].finditer(inputTagSTR)]
        for c in checkingTagLIST:
            if c.startswith(argXTagSTR) and argY in c:
                return True
            else:
                pass
    else:
        resultBOOL = "Unknown"

    return resultBOOL


if __name__ == "__main__":
    inputDICT = {"inputSTR":"任何人沒吃晚餐", "argX":"任何", "argY":"人"}               #True
    inputDICT = {"inputSTR":"老張批評了自己", "argX":"老張", "argY":"自己"}             #True
    inputDICT = {"inputSTR":"老張的爸爸批評了自己", "argX":"老張", "argY":"自己"}        #False
    #inputDICT = {"inputSTR":"老張的爸爸批評了自己", "argX":"老張", "argY":"爸爸"}        #True
    #inputDICT = {"inputSTR":"老張的爸爸批評了自己", "argX":"老張的爸爸", "argY":"自己"}   #True
    #inputDICT = {"inputSTR":"老張知道約翰喜歡自己", "argX":"老張", "argY":"自己"}        #True
    #inputDICT = {"inputSTR":"老張知道約翰喜歡自己", "argX":"約翰", "argY":"自己"}        #True


    result = CCMDchecker(inputSTR=inputDICT["inputSTR"], argX=inputDICT["argX"], argY=inputDICT["argY"])
    print("在 [{}] 一句中…".format(inputDICT["inputSTR"]))
    print("[{}] 是否 c-command [{}]？ {}".format(inputDICT["argX"], inputDICT["argY"], result))
