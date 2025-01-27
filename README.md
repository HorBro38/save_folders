# Media Skip for Ren'py
by HB38

This library allows you to add in save folders that generate based off a random seed the player is assigned on game creation, allowing you them to have a folder like structure that allows them to seperate their saves by play through attempt.  When going to the load screen, you will see a list of available play throughs/seeds/characters/etc:

<img width="665" alt="load_folders" src="https://github.com/user-attachments/assets/489657e3-8fbf-4a4b-85f2-ba6554f8f558" />

You can modify the default by adjusting the `SF_RN_NAME` variable at the top of the rpy file.  This could be the player's name, a customized character name or something they themselves choose.  If more than one folder has the same name, the second (and third…) copies of that folder will append the time of the first save in the folder to the title to make it more clear of the details of that folder.

Once in the save screen, it looks similar to the existing one except the folder name is at the top.  Just like the default page text, this can be editted by clicking on it - doing so will also update the folder name on the load page:

<img width="665" alt="slot_screen" src="https://github.com/user-attachments/assets/7d1f09b1-b7dc-4b41-b1f9-f168d3c68c92" />

Once you click into a folder, the player will only see the saves that match the seed of that folder to help them organize their saves.  On the back end, the saves are store normaly but have their seed values appended to the save name (for example, `1-1AWNT1UFYGPCU4AYFARSPQF4V6-LT1.save`).

## Customization

Just like the default save screens, these can be modified to fit the style of your game.

(going to show a custom version of the Pathfinder app here)

## Requirements

This has been tested back to Ren'py 8.2.3; but earlier versions should be compatiable as well.

## Terms of Use
Feel free to use this as you desire, credit is not necessary but always appreciated (feel free to simply credit HB38).

## Want to leave a tip?
[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/hb38_psk)
