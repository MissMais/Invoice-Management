import pyautogui 
 
positions=pyautogui.position()
s= pyautogui.click()
p =pyautogui.size()
print(p)
print(s)
print(positions)
# pyautogui.alert('This is an alert box.')
pyautogui.confirm('Shall I proceed?')