import tkinter as tk
import random, math, tkinter.messagebox as msg

#── GAME STATE ────────────────────────────────────────────────
state = {
    "day": 0, "level": 1,
    "health": 100, "max_health": 100,
    "gold": 150,
    "weapon_bonus": 0, "armor_bonus": 0,
    "inventory": {"potions": 1, "armor": [], "weapons": []},
    "enemy": None
}

ITEM_INFO = {
    "potion": "Restores 30 HP +2×(level−1).",
    "armor":  "Armor adds its AC bonus.",
    "weapon":"Weapons add their ATK bonus."
}

#── DRAW HELPERS ───────────────────────────────────────────────
def draw_sky(c, w, h, top, bot):
    r1,g1,b1 = c.winfo_rgb(top); r2,g2,b2 = c.winfo_rgb(bot)
    steps=60; dr, dg, db = (r2-r1)/steps, (g2-g1)/steps, (b2-b1)/steps
    for i in range(steps):
        nr = int(r1+dr*i)>>8; ng = int(g1+dg*i)>>8; nb = int(b1+db*i)>>8
        c.create_rectangle(0, i*h//steps, w, (i+1)*h//steps,
                           fill=f'#{nr:02x}{ng:02x}{nb:02x}', width=0)

def draw_tavern_bg(c):
    c.delete("all")
    w,h = 720,360
    # wooden walls
    c.create_rectangle(0,0,w,h, fill="#8b5a2b", width=0)
    for y in range(0,h,30):
        c.create_line(0,y,w,y, fill="#7a482a")
    # bar counter
    c.create_rectangle(0,250,w,300, fill="#5c3d21", width=0)
    # bottles
    for x in range(100,600,100):
        c.create_rectangle(x,220,x+20,250, fill="#2e8b57", outline="#1f5f3b")
    c.create_text(360, 30, text="Drunken Dragon Tavern",
                  font=("Georgia",24), fill="#f5deb3")

def draw_forest_bg(c):
    c.delete("all")
    w,h = 720,360
    draw_sky(c,w,h,"#a0d8f0","#7dc87c")
    c.create_rectangle(0,int(h*0.6),w,h, fill="#2e8b57", width=0)
    # layered trees
    for x in range(80,w,140):
        c.create_rectangle(x-10,h*0.6-80,x+10,h*0.6, fill="#8b4513", width=0)
        for dy,r,col in [(0,50,"#228b22"),(30,40,"#1e7e34"),(60,30,"#2fa84f")]:
            c.create_oval(x-r, h*0.6-80-dy-r, x+r, h*0.6-80-dy+r,
                          fill=col, width=0)

def draw_market_bg(c):
    c.delete("all")
    w,h = 720,360
    draw_sky(c,w,h,"#f0e68c","#dda0dd")
    # tents
    for x in range(120,w,240):
        c.create_polygon(x,200, x+80,200, x+40,140,
                         fill="#ff8080", outline="#aa5050")
        c.create_rectangle(x+20,200,x+60,280, fill="#fff", outline="#ccc")

def draw_knight(c,x,y,s=1):
    # helmet with visor
    c.create_oval(x-20*s,y-80*s,x+20*s,y-60*s, fill="#4a90e2", width=0)
    c.create_rectangle(x-20*s,y-70*s,x+20*s,y-65*s, fill="#356bb0", width=0)
    # plume
    c.create_line(x,y-80*s,x,y-125*s, fill="#e74c3c", width=6*s)
    # body
    c.create_rectangle(x-15*s,y-65*s,x+15*s,y+10*s, fill="#4a90e2", width=0)
    # arms
    c.create_line(x-15*s,y-45*s,x-45*s,y, fill="#4a90e2", width=8*s)
    c.create_line(x+15*s,y-45*s,x+45*s,y, fill="#4a90e2", width=8*s)
    # shield
    pts = [x-25*s,y+10*s, x-50*s,y+50*s, x-25*s,y+80*s]
    c.create_polygon(pts, fill="#bdc3c7", outline="#7f8c8d")
    # sword
    c.create_line(x+15*s,y, x+60*s,y-40*s, fill="#ecf0f1", width=6*s)
    # legs
    c.create_line(x-10*s,y+10*s,x-20*s,y+80*s, fill="#4a90e2", width=8*s)
    c.create_line(x+10*s,y+10*s,x+20*s,y+80*s, fill="#4a90e2", width=8*s)

def draw_thorinton(c,x,y,s=1):
    # dwarf behind bar
    c.create_rectangle(x-20*s,y-40*s,x+20*s,y+20*s, fill="#d35400", width=0)
    c.create_oval(x-20*s,y-80*s,x+20*s,y-40*s, fill="#d35400", width=0)
    # helmet
    c.create_arc(x-25*s,y-75*s,x+25*s,y-45*s, start=0, extent=180,
                 fill="#7f8c8d", outline="")
    # hammer in hand
    c.create_line(x+18*s,y, x+60*s,y-10*s, fill="#aaa", width=8*s)
    c.create_rectangle(x+55*s,y-15*s,x+65*s,y+5*s, fill="#7f8c8d", outline="")

def draw_generic_enemy(c,name,x,y,s=1):
    col = {"Goblin":"#27ae60","Bugbear":"#8b4513",
           "Orc":"#8b4513","Troll":"#8b4513",
           "Wyvern":"#27ae60","Dragon":"#7f0000"}[name]
    # head
    c.create_oval(x-25*s,y-75*s,x+25*s,y-45*s, fill=col, width=0)
    # eyes
    c.create_oval(x-15*s,y-70*s,x-5*s,y-60*s, fill="white")
    c.create_oval(x+5*s,y-70*s,x+15*s,y-60*s, fill="white")
    # fangs if dragon
    if name=="Dragon":
        c.create_line(x-10*s,y-45*s,x-12*s,y-25*s,fill="white",width=3*s)
        c.create_line(x+10*s,y-45*s,x+12*s,y-25*s,fill="white",width=3*s)
    # body
    c.create_rectangle(x-20*s,y-45*s,x+20*s,y+10*s, fill=col, width=0)
    # club/spikes
    if name in ("Bugbear","Troll"):
        c.create_line(x+20*s,y-20*s,x+60*s,y+30*s,fill="#654321",width=12*s)
        c.create_oval(x+55*s,y+25*s,x+65*s,y+35*s,fill="#654321",outline="")
    else:
        # claws for other beasts
        c.create_line(x+20*s,y,y+40*s,y+60*s,fill=col,width=6*s)

#── UI SETUP ──────────────────────────────────────────────────
root = tk.Tk()
root.title("Package Delivery Quest")
canvas = tk.Canvas(root, width=720, height=360)
canvas.pack()
story = tk.Label(root, font=("Georgia",14), wraplength=700, justify="left")
story.pack(pady=6)
log = tk.Label(root, font=("Arial",11), wraplength=700, justify="left")
log.pack(pady=4)
hud = tk.Frame(root); hud.pack()
hp_lbl = tk.Label(hud); hp_lbl.pack(side="left", padx=10)
gold_lbl = tk.Label(hud); gold_lbl.pack(side="left", padx=10)
enemy_lbl = tk.Label(root, font=("Arial",11)); enemy_lbl.pack()
btns = tk.Frame(root); btns.pack(pady=6)
atk = tk.Button(btns, text="Action", width=10)
ret = tk.Button(btns, text="Retreat", width=10)
bar = tk.Button(btns, text="Barter", width=10)
hid = tk.Button(btns, text="Hide",   width=10)
inv = tk.Button(btns, text="Inventory", width=10,
                command=lambda: open_inventory())
atk.grid (row=0,column=0,padx=4)
ret.grid (row=0,column=1,padx=4)
bar.grid (row=0,column=2,padx=4)
hid.grid (row=0,column=3,padx=4)
inv.grid (row=0,column=4,padx=4)

#── CORE LOGIC ─────────────────────────────────────────────────
def update_hud():
    hp_lbl.config(text=f"HP: {state['health']}/{state['max_health']}")
    gold_lbl.config(text=f"Gold: {state['gold']}g")
    if state["health"] <= 0:
        show_death()

def show_story(txt, btn_txt, cmd):
    story.config(text=txt)
    log.config(text="")
    enemy_lbl.config(text="")
    atk.config(text=btn_txt, command=cmd, state="normal")
    for b in (ret,bar,hid): b.config(state="disabled")
    update_hud()

def show_death():
    for b in (atk,ret,bar,hid): b.config(state="disabled")
    d = tk.Toplevel(root); d.title("You Died")
    tk.Label(d, text="Your quest fails...", fg="red",
             font=("Georgia",14)).pack(pady=20)
    tk.Button(d, text="Quit", command=root.destroy).pack()

def open_inventory():
    w = tk.Toplevel(root); w.title("Inventory")
    invn = state["inventory"]
    tk.Label(w, text=f"Potions: {invn['potions']}").pack(pady=2)
    tk.Button(w, text="Use Potion",
              command=lambda:[use_potion(), w.destroy()]).pack(pady=4)
    tk.Label(w, text="Armor:").pack(pady=(10,0))
    for i,(n,b,c) in enumerate(invn["armor"]):
        rb = tk.Radiobutton(w, text=f"{n} (+{b} AC)", value=i,
             command=lambda idx=i: equip_armor(idx))
        rb.pack(anchor="w")
    tk.Label(w, text="Weapons:").pack(pady=(10,0))
    for i,(n,b,c) in enumerate(invn["weapons"]):
        rb = tk.Radiobutton(w, text=f"{n} (+{b} ATK)", value=i,
             command=lambda idx=i: equip_weapon(idx))
        rb.pack(anchor="w")
    tk.Button(w, text="Close", command=w.destroy).pack(pady=8)

def use_potion():
    invn = state["inventory"]
    if invn["potions"] > 0:
        invn["potions"] -= 1
        heal = 30 + 2*(state["level"]-1)
        state["health"] = min(state["max_health"], state["health"] + heal)
        log.config(text=f"Used potion: +{heal} HP")
    else:
        msg.showinfo("No Potions","You have none!")
    update_hud()

def equip_armor(idx):
    n,b,c = state["inventory"]["armor"][idx]
    state["armor_bonus"] = b
    log.config(text=f"Equipped {n}: +{b} AC")

def equip_weapon(idx):
    n,b,c = state["inventory"]["weapons"][idx]
    state["weapon_bonus"] = b
    log.config(text=f"Equipped {n}: +{b} ATK")

def open_market():
    w = tk.Toplevel(root); w.title("Day 6 Market")
    tk.Label(w, text=f"Gold: {state['gold']}g").pack(pady=4)

    offers = [
      ("Health Potion",30,"potion",
         lambda: state["inventory"].__setitem__("potions",
                state["inventory"]["potions"]+1)),
      ("Leather Armor",50,"armor",
         lambda: state["inventory"]["armor"].append(
                ("Leather Armor",2,50))),
      ("Chainmail",100,"armor",
         lambda: state["inventory"]["armor"].append(
                ("Chainmail",4,100))),
      ("Plate Armor",180,"armor",
         lambda: state["inventory"]["armor"].append(
                ("Plate Armor",6,180))),
      ("Mythril Armor",350,"armor",
         lambda: state["inventory"]["armor"].append(
                ("Mythril Armor",9,350))),
      ("Shortsword",40,"weapon",
         lambda: state["inventory"]["weapons"].append(
                ("Shortsword",3,40))),
      ("Rapier",80,"weapon",
         lambda: state["inventory"]["weapons"].append(
                ("Rapier",5,80))),
      ("Warhammer",160,"weapon",
         lambda: state["inventory"]["weapons"].append(
                ("Warhammer",8,160))),
      ("Greatsword",250,"weapon",
         lambda: state["inventory"]["weapons"].append(
                ("Greatsword",12,250))),
      ("Sweihander",500,"weapon",
         lambda: state["inventory"]["weapons"].append(
                ("Sweihander",18,500))),
    ]

    def buy(n,c,k,fn):
        if state["gold"]<c:
            tk.Label(w,text="Not enough gold.",fg="red").pack()
        else:
            fn(); state["gold"]-=c; update_hud()
            tk.Label(w,text=f"Bought {n}: {ITEM_INFO[k]}",fg="green").pack()

    for n,c,k,fn in offers:
        f=tk.Frame(w); f.pack(fill="x",padx=10,pady=2)
        tk.Label(f,text=f"{n} — {c}g").pack(side="left")
        tk.Button(f,text="Buy",
                  command=lambda n=n,c=c,k=k,fn=fn: buy(n,c,k,fn)
                 ).pack(side="right")

    def sell(kind):
        lst = state["inventory"][kind]
        if not lst:
            msg.showinfo("Nothing",f"No {kind}."); return
        n,b,c=lst.pop(); refund=c//2
        state["gold"]+=refund; update_hud()
        tk.Label(w,text=f"Sold {n} for {refund}g",fg="orange").pack()

    tk.Label(w,text="— Sell Gear —").pack(pady=(10,0))
    tk.Button(w,text="Sell Armor", command=lambda:sell("armor")).pack(pady=2)
    tk.Button(w,text="Sell Weapon",command=lambda:sell("weapons")).pack(pady=2)
    tk.Button(w,text="Leave", command=lambda:[w.destroy(), next_stage()]).pack(pady=8)

def next_stage():
    canvas.delete("all")
    for b in (atk,ret,bar,hid): b.config(state="disabled")
    d = state["day"]

    if d == 0:
        draw_tavern_bg(canvas)
        draw_knight(canvas,150,300,1)
        draw_thorinton(canvas,550,300,1)
        show_story(
          "Thorinton the dwarf slides a wrapped package across the bar:\n"
          "'Deliver this to Waterdeep by dawn of Day 7, brave knight.'",
          "Accept Quest", next_stage
        )

    elif 1 <= d <= 5:
        draw_forest_bg(canvas); draw_knight(canvas,150,300,1)
        foe=["Goblin","Bugbear","Orc","Troll","Wyvern"][d-1]
        start_encounter(foe)

    elif d == 6:
        draw_market_bg(canvas)
        log.config(text="Day 6: The Adventurer’s Market")
        atk.config(text="Enter Market", command=open_market, state="normal")

    elif d == 7:
        draw_forest_bg(canvas)
        draw_generic_enemy(canvas,"Dragon",360,250,1.2)
        start_encounter("Dragon", hp=300, level=8)

    else:
        show_story(
          f"You triumphantly deliver the package!\n"
          f"Final Gold: {state['gold']}g   Level: {state['level']}",
          "Quit", root.destroy
        )

    state["day"] += 1
    update_hud()

def start_encounter(name, hp=None, level=None):
    stats = {"Goblin":(80,2),"Bugbear":(120,4),"Orc":(150,5),
             "Troll":(200,6),"Wyvern":(180,7),"Dragon":(300,8)}
    hp0,lv0 = stats[name] if hp is None else (hp, level)
    state["enemy"] = {"name":name,"hp":hp0,"max":hp0,"level":lv0}
    draw_generic_enemy(canvas,name,600,300,1)
    log.config(text=f"Day {state['day']}: A {name} blocks your path!")
    enemy_lbl.config(text=f"{name} HP: {hp0}/{hp0}")
    atk.config(text="Attack", command=attack, state="normal")
    for b in (ret,bar,hid): b.config(state="normal")

def attack():
    e = state["enemy"]
    dmg = random.randint(20,30) + state["level"]*2 + state["weapon_bonus"]
    e["hp"] -= dmg
    log.config(text=f"You strike {e['name']} for {dmg} dmg.")
    enemy_lbl.config(text=f"{e['name']} HP: {max(0,e['hp'])}/{e['max']}")
    if e["hp"] <= 0:
        loot = 500 if e["name"]=="Dragon" else 50
        state["gold"] += loot; state["level"] += 1
        log.config(text=log.cget("text")+f"\nYou slay {e['name']}! +{loot}g")
        state["enemy"] = None; next_stage()
    else:
        atk.config(state="disabled"); canvas.after(800, enemy_strike)

def enemy_strike():
    e = state["enemy"]
    dmg = random.randint(8,14) + e["level"] - state["armor_bonus"]
    dmg = max(1, dmg)
    state["health"] -= dmg
    log.config(text=log.cget("text")+f"\n{e['name']} hits you for {dmg} dmg.")
    update_hud()
    if state["health"]>0:
        for b in (atk,ret,bar,hid): b.config(state="normal")

def do_retreat():
    if random.random() < 0.5:
        log.config(text="You slip away safely!")
        state["enemy"] = None; next_stage()
    else:
        log.config(text="Retreat failed!") ; canvas.after(800, enemy_strike)

def do_barter():
    e = state["enemy"]
    br = random.randint(5,15)*e["level"]
    state["gold"] += br; update_hud()
    log.config(text=f"You bribe {e['name']} for {br}g.")
    canvas.after(800, enemy_strike)

def do_hide():
    if random.random() < 0.7:
        log.config(text="You vanish into shadows; enemy misses a turn.")
        for b in (atk,ret,bar,hid): b.config(state="normal")
    else:
        log.config(text="Hide failed!"); canvas.after(800, enemy_strike)

# bind extra actions
ret.config(command=do_retreat)
bar.config(command=do_barter)
hid.config(command=do_hide)

# launch
next_stage()
root.mainloop()
