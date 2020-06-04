# EFAI Inference API Sample Python Client

This demo script will do the following:
1. Login and obtain a new session key.
2. Convert a File to a base64 string.
3. Upload the File.
4. Show a list of inference.
5. Get inference results.

## Get models
```bash
$python3 efai.py -a models
                Name                               Long Name      Cost
             boneage                                Bone Age         1
  breastus_detect_v3                               Breast US         5
               mammo                             Mammography         1
diabetic_retinopathy                    Diabetic Retinopathy         1
                 cmr                             Chest X-Ray         1
          liverct_v2                                Liver CT         1
            oralpano                               Dentistry         1
          icfracture              Intertrochanteric Fracture         1
                 kub                                     KUB         2
                 bmd                    Bone Mineral Density         3
      ecg_multicat16                       Electrocardiogram         2
             brainct                                Brain CT         1
                 tcm                                      中藥         1
```

## Get a list of previous inferences
```bash
$python3 efai.py -a list -u demo -p demo
                 DateTime                    Model                                      ID
2020-06-04T04:58:12.467743                  boneage    41e0e522-e4e4-4cbb-a1a1-70627d3920a8
2020-06-03T02:57:09.258997                  brainct    62473b4a-bf08-46c6-8732-91fce5ef90dc
2020-06-02T09:28:24.222362                  brainct    4c161434-53e4-4280-bcc7-2c1a4922cdf1
```

## Make a new inference
```bash
$python efai.py -a new -u demo -p demo -m boneage -f "/tmp/image.dcm"
Inference ID: 41e0e522-e4e4-4cbb-a1a1-70627d3920a8
```

## Get a specific inference result
```bash
$python efai.py -a get -u demo -p demo -i 41e0e522-e4e4-4cbb-a1a1-70627d3920a8
        ID  Report                                                                          
         4  BONE AGE: 12.6<br><br>PROCEDURE PERFORMED: BONE AGE STUDY<br><br>TECHNIQUE: Single frontal view of the left hand.<br><br>FINDINGS:<br>Sex: F<br>Study Date: 20181230<br>Date of Birth: 20060302<br>Chronological Age: 12 years, 10 months<br><br>At the chronological age of 12 years, 10 months, using the Brush Foundation data, the mean bone age for calculation is 13 years, 0 months. Two standard deviations at this age is 21.34 months, giving a normal range of 11 years, 3 months to 14 years, 9 months (+/- 2 standard deviations).<br><br>By the method of Greulich and Pyle, the bone age is estimated to be 12 years, 6 months.<br><br>CONCLUSION:<br>Chronological Age: 12 years, 10 months<br>Estimated Bone Age: 12 years, 6 months<br><br>The estimated bone age is normal.
```
