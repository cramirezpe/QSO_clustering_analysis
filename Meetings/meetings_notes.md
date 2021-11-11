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
- [ ] Make a comparison plot between biasing models/density models in the same axis. (Without correcting the biasing model)
- [ ] Make a comparison plot between biasing models/density models but "renormalizing" bias, at first by simply re-scaling all the correlations to "fix" the bias at large scales.
- [ ] Comparison plots might be more useful if we plot the ratio of all of them against something "standard" (this could be the linear model).
- [ ] **Include the quadrupole in the plots is mandatory.**
- [ ] Study and apply redshift errors.
- [ ] For the future it would be nice to implement changes in CoLoRe code that makes the "effective bias" equal to the input bias. 