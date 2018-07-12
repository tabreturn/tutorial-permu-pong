# input types
# 1: 1-button
# 2: 2-button
# 3: analog
# 4: keyboard
input_mode = 4

# adjustable variables
display_width = int(random(500,1000))
display_height = int(random(200,600))
color_fg = '#' + hex(int(random(255)),2) + hex(int(random(255)),2) + hex(int(random(255)),2)
color_bg = '#' + hex(int(random(255)),2) + hex(int(random(255)),2) + hex(int(random(255)),2)
paddle_speed = random(10,20)
paddle_thickness = random(5,30)
paddle_length = random(15,200)
paddle_margin = random(15,100)
ball_xspeed = random(2,8)
ball_yspeed = random(2,8)
ball_speedlimit = (5,13)
ball_size = random(5,20)
wall_teleport = int(random(2))
net_width = random(1,4)
opponent_agility = random(1,8)

# leave these variables alone
ball_x = 0
ball_y = 0
paddle_y = 0
add_library('serial')
arduino = False
serve = True
opponent_paddle_y = 0

def setup():
    size(display_width, display_height)
    frameRate(60) # frames per second
    
    global opponent_paddle_y
    opponent_paddle_y = height/2 - paddle_length/2
    
    # connect to arduino
    global arduino
    print( Serial.list() )
    arduino = Serial(this, Serial.list()[1], 9600)
    
def draw():
    global ball_x, ball_y, ball_xspeed, ball_yspeed, paddle_speed, paddle_y, serve, opponent_paddle_y
    
    # theme
    noStroke()
    background(color_bg)
    fill(color_fg)
    
    # net
    rect(
      (width/2)-(net_width/2), 0,
      net_width, height
    )
       
    # teleporting walls
    if wall_teleport:
        if ball_y > height:
            ball_y = 0
        if ball_y < 0:
            ball_y = height    
    # rebounding walls
    else:
        if ball_y > height:
            ball_yspeed *= -1
        if ball_y < 0:
            ball_yspeed *= -1

    data = arduino.readString()
    
    # input type: 1 button serial data to y-coord
    if input_mode == 1:
        try: 
            newline = data.find('\n')
            digit = data[newline+1:newline+2]
            if digit == '1' and paddle_y < height:
                paddle_speed = abs(paddle_speed)
            if digit == '0' and paddle_y > 0:
                paddle_speed = abs(paddle_speed)-1
            paddle_y += paddle_speed
        except:
            paddle_y = height/2 - paddle_length/2 
            print('no connnection')

    # input type: 1 button serial data to y-coord
    if input_mode == 2:
        try: 
            newline = data.find('\n')
            digit = data[newline+1:newline+2]
            if digit == 'U' and paddle_y < height:
                paddle_speed = -paddle_speed
            if digit == 'D' and paddle_y > 0:
                paddle_speed = paddle_speed
        except:
            print('no connnection')
        paddle_y += paddle_speed
        
    # input type: analog serial data to y-coord
    if input_mode == 3:
        try:
            newline = data.find('\n')
            paddle_y = int(data[newline+1:newline+5] )
        except:
            paddle_y = 0
        paddle_y = map(paddle_y,0,1023, 0,height-paddle_length)
    
    # ball
    if serve:
        ball_x = width - paddle_margin - paddle_thickness - ball_size
        ball_y = paddle_y + paddle_length/2 - ball_size/2
        ball_xspeed = abs(ball_xspeed)*-1
    else:
        ball_x += ball_xspeed
        ball_y += ball_yspeed
    rect(
      ball_x, ball_y,
      ball_size, ball_size
    )
    
    # player paddle
    rect(
      width-paddle_margin-paddle_thickness, paddle_y, 
      paddle_thickness, paddle_length
    )
    # player paddle collision
    if ball_x+ball_size > width-paddle_margin-paddle_thickness and ball_x < width-paddle_margin \
       and ball_y > paddle_y and ball_y < paddle_y+paddle_length:
        ball_xspeed *= -1
        ball_x = width-paddle_margin-paddle_thickness-ball_size
    
    # opponent paddle
    rect(
      paddle_margin, opponent_paddle_y, 
      paddle_thickness, paddle_length
    )
    # opponent paddle collision
    if ball_x < paddle_margin+paddle_thickness and ball_x > paddle_margin \
       and ball_y > opponent_paddle_y and ball_y < opponent_paddle_y+paddle_length:
        ball_xspeed *= -1
        ball_x = paddle_margin+paddle_thickness
    # ai
    if ball_y < opponent_paddle_y+paddle_length/2:
        opponent_paddle_y -= opponent_agility
    if ball_y > opponent_paddle_y+paddle_length/2:
        opponent_paddle_y += opponent_agility

    # score
    if ball_x > width or ball_x < 0:
        if int(random(0,2)):
            ball_yspeed *= -1;
        serve = True

# keyboard input
def keyPressed():
    global paddle_speed, paddle_y, serve
    
    if keyCode == 32: # ascii code for space character
        serve = False

    if input_mode == 4:
        if keyCode == UP and paddle_y > 0:
             paddle_y -= paddle_speed
        elif keyCode == DOWN and paddle_y+paddle_length < height:
             paddle_y += paddle_speed
