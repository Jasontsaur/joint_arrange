'''排列樑柱接頭的空格與鋼筋'''
# import numpy as np
# pylint: disable=C0103

EDGE_DIST_COL=80
EDGE_DIST_BM=75
na_rebar_col=0



def arrange_col(na,x,edge,c2c): #arrange col rebar position  規則 柱筋空格位置，等距擺放
    '''arrange col rebar '''
    # 等距 2 db 設定柱筋空格位置 放在 x[]
    # 回傳 x: 柱主筋空格座標
    for _ in range(na):
        x[_]=int(edge+c2c*_)
    return x

def fit_bm(n,x,y,y0,y1): # 找尋真正可以擺放梁筋的位置
    '''找尋真正可以擺放梁筋的位置'''
    for _ in range(n):
        if x[_]<=y1 and x[_]>=y0:
            y[_]=1
        else:
            y[_]=0

def getx(element):
    ''' get x of a list'''
    return element['x']

def find_space(_x0,_x1,_db_col,_db_bm,xb,i_space):
    '''尋找可以擺放梁筋的連續空間'''
    #
    #   _x0:        輸入 起點
    #   _x1:        輸入 終點
    #   _db_col:    輸入 柱筋直徑
    #   _db_bm:     輸入 梁筋直徑
    #   xb:         輸入/回傳 梁筋空格位置
    #   i_space:    輸入/回傳 梁筋空格數量
    
    nb_rebar_col=int((_x1-_x0-_db_col)/_db_bm) #算出幾個db
    nb_rebar_col=int((nb_rebar_col+1)/2)   #放一支空一支,例如5個空格可以放3支
    tmp=((_x1-_x0-_db_col)-(nb_rebar_col*2-1)*_db_bm)/2
    for j in range(nb_rebar_col):
        xb[i_space]=int(_x0+(_db_col/2+_db_bm/2)+j*2*_db_bm+tmp)
        # print(i_space," xb:   ",xb[i_space])
        i_space=i_space+1
    return i_space

def build_runway(wid_col,wid_bma,wid_bmb,demand_rebar_col,offset_bma,offset_bmb,layout:str):
    '''解梁柱接頭平面排列'''
    # build_runway(柱寬,梁寬a,梁寬b,柱筋數,梁偏位a,梁偏位b)
    #    wid_col=1100            : 輸入 柱寬
    #    wid_bma=600             : 輸入 梁寬 a
    #    wid_bmb=750             : 輸入 梁寬 b
    #    demand_rebar_col=8      : 輸入 需求主筋根數
    #    offset_bma=100          : 輸入 偏心量 a
    #    offset_bmb=300          : 輸入 偏心量 b
    #    layout                  : 輸入 柱筋排列方式='角落' / '均佈' 內定值=角落
    #    out1                    : 回傳 梁筋直通或錨碇的狀態與座標 
    #                               [{'x':xc[_],'symbol':"●     ●"}]
    #                               [{'x':xc[_],'symbol':"══════╝"}]
    #                               [{'x':xc[_],'symbol':"═══════"}]     
    #                               [{'x':xc[_],'symbol':"╚══════"}]                   
    #    na_rebar_col            : 回傳 柱主筋空格數目 
    #
    print(wid_col,wid_bma,wid_bmb,demand_rebar_col,offset_bma,offset_bmb,layout)

    db_col=32               # 輸入 柱筋直徑 mm
    db_bm=32                # 輸入 梁筋直徑 mm

    # EDGE_DIST_COL=80 #柱筋最小邊距
    wid_effective_col=wid_col-EDGE_DIST_COL*2 #有效柱寬
    # global na_rebar_col # 必須要在這裡宣告global，才能在外部讀取數值
    if layout=='均佈':
        na_rebar_col=demand_rebar_col
    else:
        na_rebar_col=int(wid_effective_col/90)+1 # int (有效柱寬/90)+1
    
    if na_rebar_col>30:
        print("error: too many col rebar",na_rebar_col)
    c2c_rebar_col=wid_effective_col/(na_rebar_col-1) #柱鋼筋心到心距離


    # global EDGE_DIST_BM
    EDGE_DIST_BM=75                     #梁筋最小邊距
    wid_e_bma=wid_bma-EDGE_DIST_BM*2    #有效梁寬 a
    wid_e_bmb=wid_bmb-EDGE_DIST_BM*2    #有效梁寬 b
    # 用不到 na_rebar_bma=int(wid_e_bma/90)+1 # 可排列上限
    # 用不到 na_rebar_bmb=int(wid_e_bmb/90)+1
    # 用不到 c2c_rebar_bm=wid_e_bma/(na_rebar_bma-1) #梁鋼筋心到心距離 假設以a梁為準 忽略a b 之間的差異

    xc=[None]*na_rebar_col # 柱空格位置
    rebar_c=[None]*na_rebar_col # 有沒有擺放柱筋 1/0

    xc=arrange_col(na_rebar_col,xc,EDGE_DIST_COL,c2c_rebar_col)
    #
    # 檢查柱主筋是否太少根，距離太遠==>中間要放一支
    if (na_rebar_col-demand_rebar_col+1)*c2c_rebar_col>350:
        middle_bar=1
    else:
        middle_bar=0

    for i in range(na_rebar_col):
        # 計算柱筋擺放順序 order
        if i<na_rebar_col:
            if i<(na_rebar_col/2):
                order=i*2+1               #   前一半
            else:
                order=(na_rebar_col-i)*2  #   後一半
        else:
            order=0
        # 依序在空格中擺放柱筋 rebar_c[i]
        if order<=(demand_rebar_col-middle_bar):
            rebar_c[i]=1
        else:
            rebar_c[i]=0

    #   
    #   柱子中間自動放一支主筋
    #
    if middle_bar==1:
        rebar_c[int((na_rebar_col-1)/2)]=1
    #
    #   在out1中填入柱主筋
    #
    out1=[]
    for _ in range(na_rebar_col):
        if rebar_c[_]==1:
            out1=out1+[{'x':xc[_],'symbol':"●     ●",'a':0,'b':0}]
            # print("●",xc[_])
        # else:
            # print("○",xc[_])

    #
    #   在out1中填入 梁 主筋
    #

    i=0
    i_space=0   # 可以放得下幾支梁筋
    xb=[0]*30
    # na_rebar_col : 柱主筋格子數目
    x0=xc[0]    # 預防"連續空間" 之前，只有一支主筋
    while i <na_rebar_col-1:
        if rebar_c[i]==1 and rebar_c[i+1]==1:   #相鄰的格子都有主筋佔用了
            x0=xc[i]
            x1=xc[i+1]
            i_space=find_space(x0,x1,db_col,db_bm,xb,i_space)           
            i=i+1
            x0=xc[i]
           
        elif rebar_c[i+1]==0:   # 如果下一格是空的，表示這是一個連續空間的「起點」
            i=i+1
        elif rebar_c[i]==0 and rebar_c[i+1]==1: # 找到了不是空格，==>連續空間的「終點」
            x1=xc[i+1]
            # 計算空格間可以擺放梁筋數量 locals:x0,x1,db_col,db_bm,xb,i_space
            i_space=find_space(x0,x1,db_col,db_bm,xb,i_space)

            i=i+1
            x0=x1
        else:
            print("ERROR: 不應該出現這種情形")
    n_space_b=i_space   #   梁筋跑道數目總和

    y0a=offset_bma+EDGE_DIST_BM # 梁筋位置 下限
    y1a=y0a+wid_e_bma # 梁筋位置 上限
    y0b=offset_bmb+EDGE_DIST_BM # 梁筋位置 下限
    y1b=y0b+wid_e_bmb # 梁筋位置 上限


    rebar_ba=[None]*n_space_b # 有沒有擺放柱筋 1/0
    rebar_bb=[None]*n_space_b
    fit_bm(n_space_b,xb,rebar_ba,y0a,y1a)
    fit_bm(n_space_b,xb,rebar_bb,y0b,y1b)

    for _ in range(n_space_b):
        symbolout="       "
        if rebar_ba[_]==0 and rebar_bb[_]==0:
            pass
        elif rebar_ba[_]==1 and rebar_bb[_]==0:
            symbolout="══════╝"
        elif rebar_ba[_]==1 and rebar_bb[_]==1:
            symbolout="═══════"
        elif rebar_ba[_]==0 and rebar_bb[_]==1:
            symbolout="╚══════"
        out1=out1+[{'x':xb[_],'symbol':symbolout,'a':0,'b':0}]

    out1.sort(key=getx) # 這一步很重要，按照座標重新排序

    return out1
