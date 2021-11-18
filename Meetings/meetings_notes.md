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
- [ ] Add more galaxies (reduce downsampling).
- [ ] Try to get an output bias closer to the desired bias, so the correction is smaller. This can be accomplished by painting a bunch of tracers in the simulation (which is almost "free"). 


# 11/11/2021

## Status
- The objective of the project is to have mocks that better mimics the data at small scales. Current lognormal mocks based in CoLoRe work fine for lyman-$\alpha$ forest auto-correlation and cross-correlation with quasars; but we cannot study small scales or quasar auto-correlation with them. 
- We are trying to improve them by using 2LPT model for structure that is already implemented in CoLoRe, however, we may need to correct/improve at least the biasing model (how quasars are placed in cells depending on the density field) in order to get a more realistic clustering.
- César showed a first version of correlations (only monopole so far) for the three biasing models currently supported and for both lognormal and 2LPT densities. However, it was difficult to compare them and check which one works better due to different effective bias and different correlation theoretical models used. 

## Notes:
- We need some data to compare with. For this we could use real data from the quasar clustering group (SV3). But it would be interesting if we could also have the option to use eBOSS data. 
- At some point we should add redshift errors to the mock dataset before computing correlations (¿Is this a priority?).

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