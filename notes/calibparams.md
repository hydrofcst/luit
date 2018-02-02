| Param Name    | Param Description    | SUMMA module  | Range         |
| ------------- | ------------- | ------------- | ------------- |
| frozenPrecipMultip | snowfall = (1._dp - fracrain)*pptrate*frozenPrecipMultip | atmosphere | 0.5 - 1.5 
| summerLAI | maximum leaf area index at the peak of the growing season | vegetation | 0.01 - 10
| fieldCapacity | vol liq water content when baseflow begins | soil-zone | .d-07 - 100.d-07
| aquiferBaseflowRate | baseflow rate when aquifer storage = aquiferScaleFactor | soil-zone  | 0 - 0.1
| aquiferScaleFactor  | scaling factor for aquifer storage in the big bucket (m) |  soil-zone | 0.1 - 100 
| aquiferBaseflowExp  | baseflow exponent for the big bucket  | soil-zone  | 1.0- 10

### Random notes
* Rain–snow partitioning is the most critical model parameterization in a warm maritime snow environment (Wayand et al. 2016a,b). 
