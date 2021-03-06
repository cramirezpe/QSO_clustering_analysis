# 09/03/22
**snapshot**
I am having issues to run the snapshot realisation of CoLoRe for 2LPT mocks. I was able to run on lognormal (+ unclustered 2LPT). But 2LPT fails with both noRSD and RSD.

We took a look at the code, and it is important to make changes to how this modification is made:
- Generate new functions with new names for growth_factor, etc..
- I am currently modifying density.c, it is better not to modify this and keep changes in the other functions (cosmo.c).
- Make this new functions just return a hardcoded value, at first. This could be get by running a CoLoRe realisation which prints all the values for all redshfits.
- Andreu mentioned that the fact that voxel sizes will depend on redshift, there will always be a redshift dependence in the box that we won't be able to kill. Marc thinks this effect won't be relevant.

**unable to give predictions to 2LPT code now**
It seems that the 2LPT quadrupole signal cannot be explained with a "normal" range of redshifts. Recalling a previous plot:
![best_redshift](https://user-images.githubusercontent.com/58682644/153213597-fb64c2e5-84b5-479f-86ff-7e5f7ab6d113.png)
It seems that we need a really high value of redshift in order to be able to explain this behaviour. Hence making a snapshot or choosing a good value of effective redshfit won't be enough to explain the high differences (in principle).
This is something to think about. Maybe it is caused by the fact that we are combining 2LPT objects with linear velocities?

**TODO**
- [ ] Make changes to the snapshot code.
- [ ] Marc asked for a realisation with bias=1 (the same as the underlying dark matter). This requires to remove the density normalization in order to not modify the underlying value.


# 09/02/22
**non-clustered mocks**

![unclustered_monopole](https://user-images.githubusercontent.com/58682644/153211844-a479c103-86c3-49d8-9ac2-00f5366f2e7f.png)
![unclustered_quadrupole](https://user-images.githubusercontent.com/58682644/153211851-fd6bb35e-1838-4815-a192-c203775483c3.png)

As expected, linear velocites are correctly captured by our linear model. Somehow the lognormal and 2lpt realisation have small differences that shouldn't be there (they should be totally identical in principle), but nothing to worry about.

**compare again different biasing models**

For this I returned to previous analyses of lyman-alpha like boxes. They have the following distributions:

![high_3x2_600_distributions](https://user-images.githubusercontent.com/58682644/153213072-c557e7b4-56cc-4649-a5a7-f5b2d0db1aa3.png)

And the results of the clustering measurements are:

![high_3x2_600_monopole](https://user-images.githubusercontent.com/58682644/153213151-849e6727-b02c-4685-9155-b2d201ac765e.png)

![high_3x2_600_quadrupole](https://user-images.githubusercontent.com/58682644/153213160-7935cfa4-9843-4b50-8286-893c84ada72a.png)

It is curious that here the large-scale quadrupole seems to fit better the realisation by abacus than the previous runs that were built explicitly to match it (redshift and bias). 

We need a snapshot analysis and not a lightcone analysis to get rid of redshift evolution that can break our measurements. We also need to make a fit of the monopole-noRSD and then show the model for monopole+quadrupole RSD using the previous fit to see the agreement. If the agreement is really bad, we could contact abacus to mention this and ask if their models perform better.

**effective redshift of theory on different measurements**

Changing the effective redshift changes the shape of the quadrupole having better agreement with theory:

![narrow-z-effect-of-z-on-clustering-monopole](https://user-images.githubusercontent.com/58682644/153213525-a63120f0-1599-4b4d-ae28-334ecd1971d7.png)

![narrow-z-effect-of-z-on-clustering-quadrupole](https://user-images.githubusercontent.com/58682644/153213597-fb64c2e5-84b5-479f-86ff-7e5f7ab6d113.png)

This basically shows that the quadrupole is flexible when changing effective redshfit. However, we need to check if CoLoRe performs well for each redshift, and therefore we need to make a run with a snapshot.

**b and z correlation in monopole-RSD**

I was confused by the correlation between bias and effective redshift when fitting both in the monopole-RSD:

![image](https://user-images.githubusercontent.com/58682644/153214286-b628063d-169c-4bdc-a7ad-c112b361a230.png)

![z_and_b_effects](https://user-images.githubusercontent.com/58682644/153214245-e97d04e6-0850-48e1-948a-f6c7e2559c2e.png)

The answer is that there is not such an issue, there is a dependence between bias and z, and hence the correlation. Even if the relation is not linear the correlation will be one in the fit.

**NEXT STEPS**

- [ ] Build a snapshot at redshfit 1.4 with CoLoRe
- [ ] Perform fit of abacus without redshift and show performance of this fit with RSD clustering.
- [ ] Check the cosmology is exactly the same as abacus (partially, they should be the same but I'd like to check more things)
- [ ] Investigate the inclusion of 2LPT velocities (for the future).

# 03/02/22
**Repeating redshift distribution plot**

A improvement and correction to the redshift distribution plot shown last week. Now the confidence bars are set around 0, and the data is shown as points. The poisson errors have been corrected (there was a missing factor in the computation).

![normalized_redshfit_distribution](https://user-images.githubusercontent.com/58682644/152420482-87fd5949-eff3-4d12-b006-30be83bda4bf.png)

Now the dndz_randoms are consistent with the prediction (as expected). We should use this randoms from now on.

**Checking again input bias parameter vs effective bias**

New realisations have been made, showing that apparently what we have is a curve instead of a line. Therefore the only conflicting point is the 2.0 one. I made another run of points close to this one, showing no problematic behaviour:

![inb_outb_with_printed_norm](https://user-images.githubusercontent.com/58682644/152420965-a58a426c-fb48-4a6b-bdb1-ed4f2a71a966.png)

It is weird that the only difference between the ??2LPT NEW?? and the ??printed normalization?? one is the number of sources included in the simulation.  

Besides this, the points followed a well defined curve that can be fitted with a asymptote:

![fit_logn_lpt_inb_outb](https://user-images.githubusercontent.com/58682644/152421817-ec737379-969b-4d25-b963-b9171b3a428f.png)

This shows that there is no problem with the biasing.

**Normalisation factor evolution**

I have modified CoLoRe to make it print the normalisation factor used when producing biased sources: 1 + delta_k = B_k/<B_k>. (I'm plotting this parameter).

![mean_biased_density](https://user-images.githubusercontent.com/58682644/152422522-9980ee83-7445-4def-958f-e260185590ae.png)

This evolution does not correlate with the fluctuations in the redshift distribution. 

**Discusion about the old problems in the 2LPT correlations**

Now that we are confident in our randoms we can continue with the previous steps.

Continuing with the problematic 2LPT runs. Some of the ideas in order to try to understand the bad behaviour of 2LPT are:
- [ ] Perform fits with no RSD and then show RSD plots with the previous fit.
- [x] Make no-cluster correlations for 2LPT (bias=0). (They worked perfectly for the CoLoRe paper mocks).
- [ ] Check the cosmology is exactly the same as abacus.
- [ ] Investigate the inclusion of 2LPT velocities.
- [ ] Make wedges / rp vs rt plots trying to see where the 2LPT model is failing.

**NEXT STEP**

The checklist above.

# 27/01/22

**Check randoms: Redshift distribution**

The redshift distribution compared with the provided input redshift distribution.
![redshift_distribution](https://user-images.githubusercontent.com/58682644/151341678-405dd03c-649b-4973-b62a-4397d4cdb279.png)
It is not completely clear that the first plot is consistent with Poisson errors (something to look at). But now we have to understand if it is better to use randoms from dndz or randoms from data. If the (larger) scatter in data comes from cosmological fluctuations, then it is better to use the dndz one; if those fluctuations comes from the fact we are renormalizing (and killing higher scale correlations), we should use randoms from data.

Therefore it is important to understand the behaviour of this normalization.

**Check randoms: Pixel distribution**

The following plot shows the pixel occupation distribution divided by the expected value for this distribution (the x axis is sources per pixel):
![pixel_occupation_histogram](https://user-images.githubusercontent.com/58682644/151342443-675331b5-046d-43eb-9b7b-7a9df99bd725.png)
This plot does not show anything problematic.

**BIAS PARAMETER VS EFFECTIVE**

Using different randoms for the same data:
![Figure 3](https://user-images.githubusercontent.com/58682644/151343378-a8a8f998-c4a5-46a6-a2f1-bbb6082b4cc1.png)
This shows that using different randoms does not affect significantly the in_b out_b issue.

Adding a new realisation with new data (2LPT from dndz (2)). 
![new_data_new_randoms](https://user-images.githubusercontent.com/58682644/151343531-bd79d2c4-eb0e-4b92-9bce-88107378484f.png)
This shows that apparently the problem is not in the way the run was made. 

The last plot is a recomputation of a previous "normal" result:
![repeat_try6](https://user-images.githubusercontent.com/58682644/151343707-4354f3ba-9915-4eef-8336-bdf29d6bcb9b.png)
The orange dots are new realisations, they seem consistent with previous results.

Given this last plot, there is the question of whether there is no problem at all: orange, red and green seem to be consistent besides the input_bias=2 point. We should make a realisation with the input values: 2, 2.05, 3, 3.5. Which will show if there is an special issue around 2. We should combine it with the normalization paramater for the same realisation.

**NEXXT STEPS**

- [x] Check dndz poisson errors.
- [x] Check bias normalization evolution in redshift.
- [x] New 2LPT realisation with input biases around in_b=2.


# 13/01/22
C??sar generated a new 2LPT run with different randoms to check two things:
- Whether a realisation with new randoms will still have the same slop in the bias_parameter vs effective_bias plot.
- Show a plot with a wide range of bias values.

**New 2LPT run**
This new run has the same properties as the previous ones, in this case I did not run an equivalent lognormal run. The characteristics of the run are the same except for the new biases and new randoms. This run does not seem to be really reliable if one looks at the following results:

**BIAS PARAMETER VS EFFECTIVE**
I plotted input_bias vs best_bias (effective bias) for this new run (and new randoms) and compared it with previous results (both lognormal and previous 2LPT used the same old randoms).

![biasparvsbias](https://user-images.githubusercontent.com/58682644/149394933-88070331-d68f-4def-8d04-c708022f6c42.png)

The result shows that something is wrong with the realisation. In this case randoms are computed by reading the 2LPT galaxy distribution for the less-biased sources (bias_parameter=2), this choice in principle is irrelevant since all the sources have the same redshift distribution (and the sky distribution is full sky). Marc pointed out that the best way of computing randoms will be by sampling them from the input number density distribution.

This arises the question of whether the randoms are well computed or not. Some of the tests that can be done are:
- [x] Pixel occupation histogram. (Should be Poisson -> Gaussian).
- [x] Simple distribution plots. (This has been done previously).
- [x] Increase randoms. Maybe we can see a trend that shows us that having 1\:1 is not enough for data\:randoms.
- [x] Check if there is correlation between two randoms sets (scatter plot of pixel ocupation number for each pixel).
- [x] Measure the correlation of one set of randoms using another set of randoms as randoms.

**New 2LPT run multipoles**

![Figure 1](https://user-images.githubusercontent.com/58682644/149395002-84ed47a3-4308-43ca-8f5b-7dc1868e907c.png)

![Figure 2](https://user-images.githubusercontent.com/58682644/149395020-ac3a7776-b5c2-4183-b088-52e91ed4d955.png)

These two plots do not have much sense before we know what causes the problem in the plot input_bias vs best_bias, but they tell us that drastically increasing the value of bias seems to not be enough to explain the differences in the quadrupole. But this may change whenever we fixed the previous issue.

**NEXT STEPS:**
- [ ] Compute randoms from the input number density distribution.
- [ ] Check if randoms are ok.
- [ ] Compute randoms from input distribution.
- [ ] Extract normalization bias from CoLoRe.


# 23/12/21
**BIAS PARAMETER VS EFFECTIVE BIAS:**
In the last week we observed inconsistencies in this plot, showing a linear behaviour for all the CoLoRe runs but with different slope (exact same realisation, but rerun with different biases).

I made a new realisation to check if the behaviour was following the previous one and that's the case. In the attached file best_input_biases.png  I show the plot for the last 3 runs. They seem to be consistent.
![best_input_biases](https://user-images.githubusercontent.com/58682644/147234741-835d7e22-4ca1-4c90-bf9d-47d85face658.png)

I think I have a clue of what happened. At some point during the analysis, I accidentally removed my CoLoRe realisations (rm -rf in the wrong place...), a part from loosing the old CoLoRe boxes I also lost randoms, so I needed to re-generate them again. So maybe one of the following is happening:
I am not generating properly the randoms. At some point it will be nice if I can show you the code and check that everything is okay.
Generating randoms for different realisations implies taking as input sources with different bias. Maybe this affects the output. In principle it shouldn't, because the only thing I'm taking from the sources is the redshift distribution.

I also added to the plot a x=y line, which shows that the 2lpt slope seems a little bit more realistic (but not much). If you are interested, the exact best fit for both lines are:

lognormal:      best_bias(b) = 1.49 + 0.16??b

2lpt:           best_bias(b) = 1.04 + 0.38??b

**NEW VERSION OF THE USUAL PLOTS:**
In the attached files monopole.png  and quadrupole.png  I show the usual plot comparing lognormal and 2LPT correlations. Now the fitted range is 50-80 Mpc/h as Marc suggested.
I've added to the legend the best bias measured. The linear model always have the best bias for abacus (~ 2.07)

![monopole](https://user-images.githubusercontent.com/58682644/147234772-09e4b135-4f03-4124-a01e-3d9c9cf5bfae.png)

![quadrupole](https://user-images.githubusercontent.com/58682644/147234779-d59dcf42-e34f-4efa-923f-81839cb4ec0a.png)

**PLOTS WITH 2LPT MULTIBIAS:**
Extended version for the previous plots only for 2lpt are in attached files monopole_multibias.png  and quadrupole_multibias.png .
The input bias range I've chosen is not large enough to show big differences between the different realisations.

![monopole_multibias](https://user-images.githubusercontent.com/58682644/147234798-250a525a-f18d-4488-9bd2-4188768cdc60.png)

![quadrupole_multibias](https://user-images.githubusercontent.com/58682644/147234804-6859bcfd-4c98-4c09-ba1d-fbc823c85b86.png)

**NEXT STEPS:**
- [x] I will make another 2lpt realisation with a wider range of input bias and with new randoms. Using this I will be able to tell if the problem we observed in the BIAS PARAMETER VS EFFECTIVE BIAS is caused by re-computing randoms while having a better version of the last plots.
- [ ] I will try to modify CoLoRe in order to get the mean bias used as normalisation.

# 17/12/2021
- Now all the analyses are run for a narrow redshift bin (1.2-1.6), trying to match the effective bias with the abacus one. 
- Plot of input bias parameter vs effective bias show inconsistencies for reruns of the same CoLoRe realization. There is a "almost linear" relation between the input bias parameter and the effective bias; but when reruning the same CoLoRe realization this slope changes (even though matter density should be exactly the same).
- Plots of the monopole and quadrupole show slightly different bias due to the problems described before.  

# Conclusions
- Need to check what is happening with bias before continuing.
- 2lpt realization has far less power in the quadrupole than the expected, even though the effectiva bias (measured in the monopole) is really close to the abacus one. Maybe we could contact David Alonso at some point to see what he thinks about it.
- The fit of the bias should be made in a smaller region (50-80 would be ideal).

# Next steps
- [x] Understand what is happening with the unconsistent input bias parameters vs effective bias.
- [x] Investigate how the input bias parameters affects the 2lpt quadrupole. (Plotting 2lpt curves for different input bias parameters).
  - [ ] Interesting to make CoLoRe print the bias normalization value to see if there is something weird going on.
- [x] Make fits in 50-80 Mpc/h region.

# 01/12/2021
## Status
Now the Abacus measurement includes the combined correlations from 25 realisations. Showed also table with input b vs best bias. Also now jacknife is computed to get estimations. Showed a comparison of the different analysis with a similar output bias. Showed measurements with forced bias=0 to check if RSD effects are controlled.

## Conclusions:
- "Similar bias" is not enough, we should use the table input b/best bias to get the exact value of input b that we shold use to get an exact value for the best bias on the ranges (30,80) or so.
- Bias 0 measurements show a small difference between lognormal and 2LPT. This should should not happen in principle as the galaxies are randomly placed in both cases. It will be also prefered to use a very small value of bias to avoid problems in some CoLoRe steps. Also model 2 won't probably work with bias parameter set to 0.
- Jacknife errorbars should in principle agree with the errors from RMS; in the analysis they seem to be identical, which may be a problem in the code. The DESI-like error bars seem to be too large, maybe this is cause because they are QSOs. It would be better to show shaded bands around abacus sim instead of error bars for all the measurements.
- Quadrupole differences may arise because bias is not exactly the same, we should try to fix the bias first.
- Be careful with timing, having one job for each pixel is too much.
- Abacus is measured in a snapshot, this means that all the measurements are taken at exactly the same redshift (1.4). Trying to implement something similar to this in CoLoRe means:
  - Putting z=1.5 everythere in CoLoRe. This would be the better option, but we should tune two things: D(z) and f(z) along the code.
  - Generate a box in a slim redshfit bin, with tunned input dndz so I have a reasonable number density.

## Next steps:
- [x] Make runs with exactly the same output bias (by using interpolation), to compare them.
- [x] Make runs in a slim redshift bin z=(abacus-0.2, abacus+0.2), with a tuned dndz.
- [x] Show error-band instead of multiple error-bars.
- [x] Check why bias0 measurements yield small differences (catalog).
- [ ] Cahnge scripts so I don't have to run a large amount of scripts.

# 26/11/2021
## Status:
Not many updates from C??sar today. Showed the results without downsampling, showing smoother results. Also showed a first version of results with modified input bias to get output bias closer to the target bias.

## Conclusions:
- Unsure about how large are the errors in Abacus, how large is the simulation and the measurement, volume, etc...
- The method of fitting the monopole and the quadrupole with a scale factor might work for the monopole, but is extremely wrong for the quadrupole. Should search something else to compare between sims.
- We need "confident bands" in our measurements to allow us to check how our mocks will behave in a DESI like environment. -> Create confident bands for a DESI-like measurement. This can be achieved by re-scaling the current error bars:
  - Scaling for area: sky area for a DESI-like survey will be 1/3 of our current measurements, so error bars have a factor sqrt(3) extra.
  - Scaling for density: our mocks are 10 times denser than DESI. If we are shotnoise limited, we can consider the error being almost linear with the number of objects. Therefore a factor 10 extra.
- Compute error bars through jacknife instead of rms could help.

## Next steps:
- [x] Need table where one can see input_bias vs output_bias. See if there's a pattern there which allow us to know where the output bias will be for a given input bias.
- [x] Compute errors using jacknife.
- [x] Use DESI-like errors for our measurements.
- [x] Share our best mock with the Abacus team and ask them for larger/better(?) Abacus measurements. Or at least precise information about the current measurements.
- [ ] Pending things:
  - [ ] Define goals for project (18/11/2021)
  - [ ] Redshift errors (11/11/2021)

# 18/11/2021
## Status:
- Showed plot comparing the linear model used for CoLoRe paper (without lognormal transformation applied). This shows that SV3 results are too noisy and can't be used now. The "big" difference in abacus results may be caused by different considerations with respect to **redshift errors**. It could be caused by bias, but this would be compensated by a different growth factor.
- Showed a comparison of the abacus results with lognormal and 2lpt mocks for the three different biasing models. If bias model is different from 1, the results improve by much, adding fingers of god maybe could improve that so **checking how they dealt with this in abacus is important**. It won't be difficult to add this to the linear model and some of the simulations. 
- Showed a similar comparison as the previous one but re-scaling all the correlations to fit the clustering of the linear model at scales about 30-80 Mpc/h.
- These plots need:
  - Increase the number of galaxies to improve the measurements. 
  - Make better plots by maybe removing error bars and only showing the errorbar for one of the measurements.

## Conclusions:
- 2LPT is interesting because it offers "extra" things as 3-point correlation function, but it is good if we get a good lognormal model that works.
- We are shotnoise limited. 
- We usually talk about biasing model when populating cells in our simulations. This is sometimes confusing because it is not true that we can preserve the bias for all cases. But we should find a way of getting good output bias.

## Next steps:
- [ ] Define clearly what is our goal with this project. What we want to obtain, where to stop.
  Brainstorming:
  - BAO with Lyman alpha quasars.
  - Quasar BAO at z = 1.5
  - cross correlation QSO Lya at 1.5
  - 3x2 analyses at high redshift.
- [ ] Add redshift errors to the plots and models.
- [x] Add more galaxies (reduce downsampling).
- [x] Try to get an output bias closer to the desired bias, so the correction is smaller. This can be accomplished by painting a bunch of tracers in the simulation (which is almost "free"). 


# 11/11/2021

## Status
- The objective of the project is to have mocks that better mimics the data at small scales. Current lognormal mocks based in CoLoRe work fine for lyman-$\alpha$ forest auto-correlation and cross-correlation with quasars; but we cannot study small scales or quasar auto-correlation with them. 
- We are trying to improve them by using 2LPT model for structure that is already implemented in CoLoRe, however, we may need to correct/improve at least the biasing model (how quasars are placed in cells depending on the density field) in order to get a more realistic clustering.
- C??sar showed a first version of correlations (only monopole so far) for the three biasing models currently supported and for both lognormal and 2LPT densities. However, it was difficult to compare them and check which one works better due to different effective bias and different correlation theoretical models used. 

## Notes:
- We need some data to compare with. For this we could use real data from the quasar clustering group (SV3). But it would be interesting if we could also have the option to use eBOSS data. 
- At some point we should add redshift errors to the mock dataset before computing correlations (??Is this a priority?).

## To-Do:
The main objective for next week is to create plots that can enable us to identify what is failing in each of the mocks, and then be able to correct what is wrong.
- [x] Make a comparison plot between biasing models/density models in the same axis. (Without correcting the biasing model)
- [x] Make a comparison plot between biasing models/density models but "renormalizing" bias, at first by simply re-scaling all the correlations to "fix" the bias at large scales.
  > Done by re-scaling all the correlations to have similar power at some scales.
- [x] Comparison plots might be more useful if we plot the ratio of all of them against something "standard" (this could be the linear model).
  > Done even though it wasn't particularly useful.

- [x] **Include the quadrupole in the plots is mandatory.**
- [ ] Study and apply redshift errors.
- [ ] For the future it would be nice to implement changes in CoLoRe code that makes the "effective bias" equal to the input bias. 
