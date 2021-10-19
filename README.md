# AI_Project_abortion

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li><a href="#Download">Download</a></li>
    <li><a href="#Activate-enviroment-with">Activate enviroment with</a></li>
    <li><a href="#in-jupyter">in jupyter</a></li>
    <li><a href="#Files">in jupyter</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

### Download
1.  download anaconda 
2.  download jupyter lab 3.0.11
3.  download [glove.twitter.27B.200d.txt](https://www.kaggle.com/fullmetal26/glovetwitter27b100dtxt/activity) from kaggle.
4.  download the [AI_project](https://github.com/RehamFarhat/AI_Project_abortion/tree/main/AI_project) folder from the [repo](https://github.com/RehamFarhat/AI_Project_abortion)

create a new folder and name it pretraind_emmbedings and add it to the AI_project folder, then move the glove.twitter.27B.200d.txt file to it.


### Activate enviroment with
in the conda prompt write:
```sh
activate AI_env
   ```
   
### Run With
after you activate the enviroment run the following 
```sh
jupyter lab
   ```

### in jupyter
run the code in its order.
if you intend to run the map code, please delete the files tweets.tsv and tweets_tmp.tsv and then run the relevant code or skip the part of Tweet data creation and continue to next part (Data loader of the tweets).

### Files
1.  **implementations/ tweets_extractor.py**: includes the implementation of
extracting tweets related to abortion, the extracting based on a list of hashtags
using the twitter API.
2. **implementations/tweets_location.py** : this file includes the implementation of
extracting additional data for tweets test and train data set, using twitter API.
3. **implementations/models.py:**
This file holds the implementation of all the models and different parts of them.
4.  **implementations/training.py:**
This file holds the training and evaluation functions of the models
5.  
6. 
7. 
8. 
9. 
10.
11.
<!-- CONTACT -->
## Contact

Reham Farhat- reham.farhat@campus.technion.ac.il

Yousef Tannous - youseft@campus.technion.ac.il
