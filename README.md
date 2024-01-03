# 2millionpuzzle.hydra
Piece tagging and profiling companion for the [Two Million Dollar Puzzle](https://www.twomillionpuzzle.com), built with [Django 4](https://docs.djangoproject.com/en/4.0). It is meant to be run on your local machine, though it could also be hosted if you want to do that.

After finishing the edge of my puzzle and then running out of steam, I decided to build this tool to help me solve the remainder. Hopefully it will be useful to anyone else masochistic enough to go through the tedium of cataloguing all the pieces (which took me several hours).

And here is the finished puzzle. I won $1; the effort was worth every penny!
![solved puzzle](/etc/solved.jpg)

> # Important note
> I believe the die cut is the same for all puzzles -- this means that your puzzle should have the same shape pieces
> in the same spots in the grid as mine (though the picture may be rotated). So you can use the shape placeholders
> from my grid to solve your puzzle. The grid included in the repo (in base64) should be complete.

### The Grid

If you don't want to spend the time cataloguing pieces, perhaps simply a diagram of the shape and orientation of every piece will help you along. 

![grid](/etc/grid.png)
*You will note that the edge pieces look a bit like interior pieces with their heads cut off. There's a good reason for that!*

## Donations

I aspire to one day become an independent software/game/puzzle developer so that I can have the free time I need to start a permaculture food forest, as part of an ongoing effort to [beat Crohn's disease](https://weirdmidnightsandwich.wordpress.com). As such, if you find this software useful, any token of appreciation would be most... appreciated!

- [ko-fi](https://ko-fi.com/sycdan): `sycdan`
- [BTC](https://bitcoin.org/en/how-it-works): `bc1qvzcfrj5ckqfwle6zgjt9f5ejs298qm09qj0u3q` or `1D37DyEFzF9bEGvqaDjkK8F552wPuJqM3M`
- [ETC](https://ethereumclassic.org): `0x8955b5aDe5C237cf89B0e03487dde8C805215a0e`
- [DigiByte](https://www.digibyte.org/en-us): `DRsxaQHyATfUKEobLZU1oUmZEpjbc8sUV1`
- [Cardano](https://cardano.org/what-is-ada): `addr1q89788yemeqgjluymwdzyjppcg0p6mw0c40s48932rmuksktuwwfnhjq39lcfku6yfyzrss7r4kul32lp2wtz58hedpqr7ukau`
- [DogeCoin](https://dogecoin.com/): `DJ7D82GcEujTGXMtF722HWKEZPPfd4wky2`

## Setup

Note: this has only been tested on Windows 10 with [git bash](https://git-scm.com/download/win) and [Python 3](https://www.python.org/downloads).

```bash
pip install virtualenv
virtualenv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
./manage.py migrate
./manage.py seedgrid
./manage.py createsuperuser
```

Creating a superuser is necessary to access Django Admin.

Optionally, you can create a `.env` file in the root in order to override values in `settings.py`.

## Preparation

Before the tool can be useful, all of the pieces and their metadata must be entered into the database.

The first step is to sort the pieces into piles by their shape and then write numbers on their backs, starting from 1 for each shape. The combination of shape and number provides a unique identifier for each piece, e.g. `3-13` is the piece with 3 heads that has "13" on the back.

After this, you need to photograph all of the pieces, in the same orientation for each shape. Orient them as shown below. I assigned each shape a 1-character key code, largely based on their number of heads, for ease of reference.

### `1` (1 head)
![1](/media/images/shapes/1.png)
### `2` (2 heads)
![2](/media/images/shapes/2.png)
### `3` (3 heads)
![3](/media/images/shapes/3.png)
### `4` (4 heads)
![4](/media/images/shapes/4.png)
### `c` (classic 2-head puzzle piece)
![c](/media/images/shapes/c.png)
### `x` (0 heads)
![x](/media/images/shapes/x.png)

The piece pictures should be placed in `./media/uploaded_images`, named in the format of `{shape_key}-{number}.jpg`, e.g. `2-69.jpg`. I used [PowerRename](https://learn.microsoft.com/en-us/windows/powertoys/powerrename) to achieve this.

After this is done, the pieces must be added to the database:

```bash
./manage.py seedpieces
```

Then comes the really tedious part: inputting the piece edge data.

### Data Entry

Go to [`http://localhost:8000/admin/core/piece`](http://localhost:8000/admin/core/piece)

For each piece, go to its detail page (click the cell name in the list, e.g. `1,1`) and fill in the appropriate directional boxes (see [screenshot](#django-admin)). You can also crop the image if necessary to make the grid look better.

I mostly only labeled heads and limbs, as below, and not the holes where heads would go... you may choose to do it differently, though. In any case, you need to input the colours you see around the edges of the piece, so that you can have something to filter on when you are looking for candidate pieces.

![django admin - pieces](/etc/edge-labels.png)
*Note that the holes are empty.*

Currently, each colour needs to be represented by a single character. I used these: `b, r, o, y, g, u` (where `u` is bl**u**e -- thanks MtG!)

## Usage

```bash
./manage.py runserver
```

Go to [`http://localhost:8000`](http://localhost:8000)

- Click on a grid cell you want to place a piece in
- Use the filters above to narrow down the list of pieces
- Click on the piece to place it
- Repeat ad nauseam

## Screenshots

### Main Interface

At the top are the controls to set the expected shape and orientation of a given grid cell.
Then are the controls to filter the available pieces -- the candidates are red because they have already been used, and `Include Used` is checked.
The grid at the bottom shows all placed pieces as well as any cells where the shape/orientation of the piece that will go there has been established. 
![all controls](/etc/screenshots/index.png)

### Django Admin

This is the interface where pieces are added.
![django admin - pieces](/etc/screenshots/admin-shapes.png)

## Contributions

PRs are welcome! Unless there's significant interest, I probably won't develop this further as I no longer need it, even though there were some potentially cool things I wanted to do with it (which you may find bits of in the code).

## F.A.Q

- > The interface looks as though a child made it.
  - Firstly, that's not a question.
  - Secondly, thanks for noticing! I am very much still a child at heart!
  - Thirdly, seriously, I will always be a function-over-form guy, so it doesn't bother me.
- > Can I scan your QR code?
  - Have at it, bub.
