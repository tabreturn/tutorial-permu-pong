# https://github.com/tigoe/MakingThingsTalk2/blob/master/chapter2/project2/MonskiPong/MonskiPong.pde

# input types
# 1: 1-button
# 2: 2-button
# 3: analog
# 4: keyboard
input_mode = 4

# adjustable variables
display_width = 800
display_height = 600
color_fg = '#FFFFFF'
color_bg = '#000000'
paddle_speed = 12
paddle_thickness = 10
paddle_length = 80
paddle_margin = 80
ball_xspeed = 6
ball_yspeed = 2
ball_speedlimit = 20
ball_size = 10
wall_bounciness = 1 # for no gain/loss in speed use 1
wall_teleport = False
net_width = 5

# leave these variables alone
ball_x = 0
ball_y = 0
paddle_y = 0
add_library('serial')
arduino = False

def setup():
    size(display_width, display_height)
    frameRate(30) # frames per second
    
    # connect to arduino
    global arduino
    print( Serial.list() )
    arduino = Serial(this, Serial.list()[1], 9600)
    
def draw():
    global ball_x, ball_y, ball_xspeed, ball_yspeed, paddle_speed, paddle_y
    
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
        if ball_x+ball_size > width:
            ball_x = 0
        if ball_x < 0:
            ball_x = width
        if ball_y+ball_size > height:
            ball_y = 0
        if ball_y < 0:
            ball_y = height    
    # rebounding walls
    else:
        if ball_x+ball_size > width:
            ball_xspeed *= -1 * wb
            ball_yspeed *= wb
        if ball_x < 0:
            ball_xspeed *= -1 * wb
            ball_yspeed *= wb
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
        else:
            print('score')

# keyboard input
def keyPressed():
    global paddle_speed, paddle_y

    if input_mode == 4:
        if keyCode == UP:
             print('up')
             paddle_y -= paddle_speed
        elif keyCode == DOWN:
             print('down')
             paddle_y += paddle_speed
               
