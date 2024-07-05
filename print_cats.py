with open("cats/closed.txt", "r") as l:
  with open("cats/open_rev.txt", "r") as r:
    l_lines = [line.strip() for line in l.readlines()]
    r_lines = [line.strip() for line in r.readlines()]
    with open("cats/closed_open.txt", "a") as new:
      for l_line, r_line in zip(l_lines, r_lines):
        new.write(f"{l_line}{" "*50}{r_line}\n")
        print(l_line, " "*50, r_line)