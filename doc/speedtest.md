# speedtest #

desitest/bin/speedtest provides timing benchmarks for
  * pixsim (desisim + specter)
  * extraction (desispec + specter)
  * PSF fitting (specex)
  * redshift fitting (redrock)

## Running speedtest ##

```
#- Get the speedtest code + input data
cd $SCRATCH
git clone https://github.com/desihub/desitest
cd desitest
cp -r /global/project/projectdirs/desi/spectro/testdata/speedtest/0.1 data

#- Until the branch is merged, checkout the speedtest branch
git checkout speedtest

#- Configure a version of DESI code to test, e.g.
source /project/projectdirs/desi/software/desi_environment.sh 17.12

#- run the speedtest
salloc -N 1 -t 2:00:00 --qos interactive -C haswell
bin/speedtest -o hsw.yaml

salloc -N 1 -t 2:00:00 --qos interactive -C knl
bin/speedtest -o knl.yaml

#- compare results
bin/compare-speedtest hsw.yaml knl.yaml
```

## Future work ##

After we have converged that these benchmarks are the ones we want, we'll
run this for every DESI software release and keep the results so that we
can run performance regression testing prior to new releases.
