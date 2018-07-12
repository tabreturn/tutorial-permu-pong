# https://github.com/tigoe/MakingThingsTalk2/blob/master/chapter2/project2/MonskiPong/MonskiPong.pde

# input types
# 1: 1-button
# 2: 2-button
# 3: analog
# 4: keyboard
input_mode = 4

# adjustable variables
display_width = int(random(200,1000))
display_height = int(random(200,1000))
color_fg = '#' + hex(int(random(255)),2) + hex(int(random(255)),2) + hex(int(random(255)),2)
color_bg = '#' + hex(int(random(255)),2) + hex(int(random(255)),2) + hex(int(random(255)),2)
paddle_speed = random(5,30)
paddle_thickness = random(5,30)
paddle_length = random(15,200)
paddle_margin = random(15,200)
ball_xspeed = random(2,20)
ball_yspeed = random(1,10)
ball_speedlimit = random(12,25)
ball_size = random(5,20)
wall_bounciness = random(0.8,1.8) # for no gain/loss in speed use 1
wall_teleport = int(random(2))
net_width = random(2,12)

# leave these variables alone
ball_x = 0
ball_y = 0
paddle_y = 0
add_library('serial')
arduino = False
serve = True

def setup():
    size(display_width, display_height)
    frameRate(30) # frames per second
    
    # connect to arduino
    global arduino
    print( Serial.list() )
    arduino = Serial(this, Serial.list()[1], 9600)
    
def draw():
    global ball_x, ball_y, ball_xspeed, ball_yspeed, paddle_speed, paddle_y, serve
    
    # theme
    noStroke()
    background(color_bg)
    fill(color_fg)
    
    # net
    rect(
      (width/2)-(net_width/2), 0,
      net_width, height
    )
    
    # rebounding wall bounciness
    if sqrt(ball_xspeed*ball_xspeed + ball_yspeed*ball_yspeed) < ball_speedlimit:
        wb = wall_bounciness
    else:
        wb = 1
    
    # teleporting walls
    if wall_teleport:
        if ball_y+ball_size > height:
            ball_y = 0
        if ball_y < 0:
            ball_y = height    
    # rebounding walls
    else:
        if ball_y+ball_size > height:
            ball_yspeed *= -1 * wb
            ball_xspeed *= wb
        if ball_y < 0:
            ball_yspeed *= -1 * wb
            ball_xspeed *= wb


    data = arduino.readString()
    
    # input type: 1 button serial data to y-coord
    if input_mode == 1:
        try: 
            newline = data.find('\n')
            digit = data[newline+1:newline+2]
            if digit == '1':
                paddle_speed *= -1
        except:
            print('no connnection')
        paddle_y += paddle_speed


    # input type: 1 button serial data to y-coord
    if input_mode == 2:
        try: 
            newline = data.find('\n')
            digit = data[newline+1:newline+2]
            if digit == 'L':
                paddle_speed = -paddle_speed
            if digit == 'R':
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
        ball_x = width - paddle_margin - ball_size
        ball_y = paddle_y + paddle_length/2 - ball_size/2
    else:
        ball_x += ball_xspeed
        ball_y += ball_yspeed
    rect(
      ball_x, ball_y,
      ball_size, ball_size
    )
    
    # paddle
    rect(
      width-paddle_margin, paddle_y, 
      paddle_thickness, paddle_length
    )
    
    # paddle collision
    if ball_x+ball_size > width-paddle_margin:
        if ball_y > paddle_y and ball_y < paddle_y + paddle_length:
            ball_xspeed *= -1

    # score
    

# keyboard input
def keyPressed():
    global paddle_speed, paddle_y, serve
    
    if keyCode == 32: # ascii code for space character
        serve = False

    if input_mode == 4:
        if keyCode == UP:
             paddle_y -= paddle_speed
        elif keyCode == DOWN:
             paddle_y += paddle_speed
               
