# Watch Life

If you're fascinated by mechanical watches, you might also enjoy a side project of mine. I've created an "analog" watch in [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) (GoL)--with a twist. I wanted the design to be small enough so you can see the inner workings without having to zoom in, hence the name *Watch Life*. 

To give you an idea of its size, [my design](https://copy.sh/life/?gist=5368d00b4e8329109a0af23dfdc85829&step=4) fits snugly in a 640 x 640 grid, making it about 165 times smaller than this GoL [digital clock](https://copy.sh/life/?gist=ca8ca84fd5f6ff82c29f7804061f547b&step=512); my watch is pasted in the top left corner for comparison.[^1]

## Gallery

To see the watch in action, you can run it at ~normal speed [here](https://copy.sh/life/?gist=5368d00b4e8329109a0af23dfdc85829&step=4), or sped up [here](https://copy.sh/life/?gist=5368d00b4e8329109a0af23dfdc85829&step=4096).

In the spirit of high horology, this design requires some training to tell the time. There are three readout mechanisms: traditional hour markers, quarter hour markers (four corners), and an analog inner dial. Both the hour and quarter hour markers are "jump" style. The inner dial is an analog display that indicates how much time remains before the next quarter hour. Roughly speaking, the number of [gliders](https://conwaylife.com/wiki/Glider) in the stream measures minutes (0-15), and its phase can be used to estimate seconds.

![watch_420](https://github.com/pmerolla/watch-life/assets/3480196/d1b720ad-2072-42fd-b6cb-274b3fa94d86)

*Annotated readout. In this instance it is 4:20:48, which can be seen by the highlighted hour (4 o'clock), quarter hour (+15 minutes in bottom right), and inner dial (+5 minutes and 48 seconds). Note one way to estimate the time from the inner dial is to measure the length of the glider stream when it hits the end (yellow highlighted path). There are markers spaced around the inner dial that indicate the minutes and seconds. Because of space constraints, the markers are broken into three 5 minute groups. In this case, the stream just passed the first 5 minute group, and landed near a marker indicating ~45 sec.*

In practice, a quick glance will tell you the hour and quarter hour almost instantly. And typically within a few seconds of staring, you can estimate how many gliders are in the inner loop to gauge the approx time within the quarter hour. This one takes some practice!

### Watch Life in action

I've also included a video highlight reel below. For a better experience, I highly recommend downloading `watch.rle` directly and using [Golly](https://golly.sourceforge.io/)!

**Transition from 11:59 to 12:00. Running 8x real time.**

https://github.com/pmerolla/watch-life/assets/3480196/eadbfd15-5e62-4961-bfb5-e5b9e5256fb1

*Play-by-play action: Around 1 second, a 45 degree line of gliders jumps from the top left corner (marking the last quarter hour) to the top right corner (marking the first quarter hour). Next, around 1 to 2 seconds, 12 "control signal" gliders fan out across the watch and make their way to the hour markers, deselecting "11" while highlighting "12". Finally, the inner dial gets cleared out at 5 seconds, and at 6 seconds starts producing gliders in groups of 3 indicating that the new quarter hour has started; i.e., the more the inner ring fills up, the more time has passed.*

**12 hours in 10.5 seconds. Running 4,096x real time.**

https://github.com/pmerolla/watch-life/assets/3480196/0bc4ef37-ed39-48f7-9529-66b7872e988f

*When we speed up the simulation by 4096, you can see the watch do a full cycle in under 11 seconds. Note the inner analog dial is difficult to see at such a fast update rate.*

## Can I use this as an actual timepiece?

Yes! 

I've had my watch running on an old laptop for weeks on end. To set the time without a lot of hassle, I modified Golly to sync with the system clock. Check it out in action.

**Displaying the time via automatic syncronization with the system clock.**

https://github.com/pmerolla/watch-life/assets/3480196/d5b2db56-86af-4bbe-90e9-a8ea8aaab2b7

*Modified version of Golly to automatically sync to the system clock (shown on right as a clock widget). At the start, the GoL watch is at 0:0:0 (top left menu bar) and the system clock is 9:51:42. To catch up, the simulation starts to rapidly advance in bursts until the two are nearly in sync (around 44 seconds into the video). From then on, the two clocks are more or less kept in sync via slight adjustments to the simulation speed.*

## Specs

* **Speed**
  * Watch designed to run at 60 frames per second (fps), which is a fun speed to watch, and is also a common refresh rate on many screens. 
  * Simulation is periodic every 60 * 60 * 60 * 12 = 2,592,000 steps. Try it!
* **Size**
  * 632 x 631 grid.
* **Jump hour movement**
  * Four [glider guns](https://en.wikipedia.org/wiki/Gun_(cellular_automaton)) produce a glider every hour (216,000 steps). Each glider fans out to hit three "hour" markers.
  * Hour markers use a set / reset latch that each have internal divide by 12 counters. This ensures only one marker is active at a time.
  * Similar technique is used for quarter hour display.
* **Analog inner dial**
  * Uses two glider guns with carefully chosen periods to create an analog stream of gliders.

## Personal side notes

Constraining the grid size to 640 x 640 made this design significantly more complex than I expected. There were moments when I nearly threw in the towel. 

Here's one such story. 

I had my heart set on an analog readout for minutes and seconds. After going through a number of prototypes, I settled on an approach that required two very particular guns with periods of 2,250 and 2,160 (see below for why). This was a show stopper since I couldn't find them anywhere, and not for lack of trying!

Late one night, just by chance, I stumbled on [this](https://catagolue.hatsya.com/textcensus/b3s23/synthesis-costs/gun) file from a relatively obscure [site]([https://catagolue.hatsya.com/textcensus/b3s23/synthesis-costs/gun](https://catagolue.hatsya.com/home)) that catalogues life patterns through random search. From this file, I got the first clue that these guns do in fact exist! Hot on the trail and through a bit of url hacking, I was finally able to locate them on these pages: [p2250](https://catagolue.hatsya.com/census/b3s23/synthesis-costs/gun?offset=1600) and [p2160](https://catagolue.hatsya.com/census/b3s23/synthesis-costs/gun?offset=2300). One of many minor miracles that pushed this project over the edge.

### Inner dial design ###

Here was my concept for the inner dial: I started from the idea to use a set / reset latch to drive the analog display. Specifically, the latch would output a stream of gliders when "set", and stop the stream when "reset". This way I could represent time by controlling the number of gliders. But how?

To achieve this, I realized if I could wire up the set and reset ports of the latch to glider guns with slightly offest periods, then this would have the desired effect. In essence it would create a phase precession that would translate into the length of the glider stream. For example at the start, the latch would be set and reset simultaneously, thus producing no gliders. But in the next period (~30 seconds later), the latch is reset at a slight offset, and now a short chain of gliders are produced. This continues every period where more and more gliders are produced, creating longer and longer chains until the guns sync back up again (after 15 minutes). It's basically a beat frequency phenomenon.

In my specific case, I needed the cycle to repeat every 15 minutes, or 54,000 steps (60 x 60 x 15). If you work out the gun periods that you need, the best option is to have one gun produce 24 gliders in 54,000 steps, and the other produce 25 gliders in the same time. These are the only integers that are offset by 1 that evenly divide 54,000. Therefore the required periods of the guns are 2,250 and 2,160. 

Putting it all together you get the final design below. I like that there's a bit of empty space here. It makes the core of the watch feel less crowded.

**Analog inner dial: Two guns with offest periods hitting a latch. Running at 8x real time.**

https://github.com/pmerolla/watch-life/assets/3480196/dedae058-b5d2-4edd-a27d-1200a9166d2c

Needless to say, this project owes much to the vibrant online GoL community for their inspirational projects and resources. As far as I know, I did not invent any novel patterns in this design. If there's anything interesting here at all, it's how the pieces come together to track time.

I share links below to projects that I found useful. Enjoy!

- [conwaylife](https://conwaylife.com/wiki/)
  - Goto for everything life related.
- [digital-logic-game-of-life](https://nicholas.carlini.com/writing/2020/digital-logic-game-of-life.html)
  - Nice expo of digital logic gates.
- [connways-game-of-life](https://www.alanzucconi.com/2020/10/13/conways-game-of-life/)
  - Inspiration for set reset latches.
- [Syntheses Catagolue](https://catagolue.hatsya.com/syntheses)
  - Incredible resource for finding non-common patterns. I stumbled on this late one night and it saved the project from being shelved.

[^1]: It is worth pointing out that the GoL digital clock design was **not** targetting a compact design, and the author describes possible optimizations [here](https://codegolf.stackexchange.com/questions/88783/build-a-digital-clock-in-conways-game-of-life). I'm showing it simply as a reference point, since it is the only other functioning time piece I am aware of in GoL.
