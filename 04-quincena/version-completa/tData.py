'''
Crea una libreria que contiene en una función los dos algoritmos juntos: el simple y el general.
'''

from cffi import FFI
ffibuilder = FFI()

ffibuilder.set_source("tData",
    '''
    #include <stdio.h>
    #include <string.h>

    void tData_general(void* src, void* dest, size_t typesize, size_t sub_shape[], size_t shape[], size_t dimension, size_t inverse) {

        size_t MAX_DIM = 8;
        size_t DIM = dimension;


        size_t dim[MAX_DIM], sho[MAX_DIM], shp[MAX_DIM], sub[MAX_DIM];
        size_t inc;

        for (size_t i = 0; i < MAX_DIM; i++) {

            if (i < DIM) {
                dim[i] = 1;
                sho[DIM - i - 1] = shape[i];
                sub[DIM - i - 1] = sub_shape[i];
                shp[DIM - i - 1] = shape[i]/sub_shape[i]*sub_shape[i];

            } else {

                dim[i] = 0;
                shp[i] = 1;
                sub[i] = 1;
                sho[i] = 1;

            }
        }

        size_t cont = 0;
        size_t J = 0;
        size_t K = 0;
        size_t L = 0;

        if (inverse == 0) {
            while (K < shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*shp[6]*shp[7]){

                if (((K + cont)%sho[0] >= sho[0] - sho[0]%sub[0])
                    || ((K + cont)%(sho[0]*sho[1])/(sho[0]) >= sho[1] - sho[1]%sub[1])
                    || ((K + cont)%(sho[0]*sho[1]*sho[2])/(sho[0]*sho[1]) >= sho[2] - sho[2]%sub[2])
                    || ((K + cont)%(sho[0]*sho[1]*sho[2]*sho[3])/(sho[0]*sho[1]*sho[2]) >= sho[3] - sho[3]%sub[3])
                    || ((K + cont)%(sho[0]*sho[1]*sho[2]*sho[3]*sho[4])/(sho[0]*sho[1]*sho[2]*sho[3]) >= sho[4] - sho[4]%sub[4])
                    || ((K + cont)%(sho[0]*sho[1]*sho[2]*sho[3]*sho[4]*sho[5])/(sho[0]*sho[1]*sho[2]*sho[3]*sho[4]) >= sho[5] - sho[5]%sub[5])
                    || ((K + cont)%(sho[0]*sho[1]*sho[2]*sho[3]*sho[4]*sho[5]*sho[6])/(sho[0]*sho[1]*sho[2]*sho[3]*sho[4]*sho[5]) >= sho[6] - sho[6]%sub[6])
                    || ((K + cont)%(sho[0]*sho[1]*sho[2]*sho[3]*sho[4]*sho[5]*sho[6]*sho[7])/(sho[0]*sho[1]*sho[2]*sho[3]*sho[4]*sho[5]*sho[6]) >= sho[7] - sho[7]%sub[7])){

                        memcpy(&dest[(K + cont) * typesize], &src[(K + cont) * typesize], typesize);
                        cont = cont + 1;

                } else {

                    L = K + cont;

                    J = dim[0]*((K)%sub[0] + K/(sub[0]*sub[1]*sub[2]*sub[3]*sub[4]*sub[5]*sub[6]*sub[7])%(shp[0]/sub[0])*sub[0])
                        +
                        dim[1]*(K/(sub[0])%sub[1]*shp[0] + K/(shp[0]*sub[1]*sub[2]*sub[3]*sub[4]*sub[5]*sub[6]*sub[7])%(shp[1]/sub[1])*shp[0]*sub[1])
                        +
                        dim[2]*(K/(sub[0]*sub[1])%sub[2]*shp[1]*shp[0] + K/(shp[0]*shp[1]*sub[2]*sub[3]*sub[4]*sub[5]*sub[6]*sub[7])%(shp[2]/sub[2])*shp[0]*shp[1]*sub[2])
                        +
                        dim[3]*(K/(sub[0]*sub[1]*sub[2])%sub[3]*shp[0]*shp[1]*shp[2] + K/(shp[0]*shp[1]*shp[2]*sub[3]*sub[4]*sub[5]*sub[6]*sub[7])%(shp[3]/sub[3])*shp[0]*shp[1]*shp[2]*sub[3])
                        +
                        dim[4]*(K/(sub[0]*sub[1]*sub[2]*sub[3])%sub[4]*shp[0]*shp[1]*shp[2]*shp[3] + K/(shp[0]*shp[1]*shp[2]*shp[3]*sub[4]*sub[5]*sub[6]*sub[7])%(shp[4]/sub[4])*shp[0]*shp[1]*shp[2]*shp[3]*sub[4])
                        +
                        dim[5]*(K/(sub[0]*sub[1]*sub[2]*sub[3]*sub[4])%sub[5]*shp[0]*shp[1]*shp[2]*shp[3]*shp[4] + K/(shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*sub[5]*sub[6]*sub[7])%(shp[5]/sub[5])*shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*sub[5])
                        +
                        dim[6]*(K/(sub[0]*sub[1]*sub[2]*sub[3]*sub[4]*sub[5])%sub[6]*shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5] + K/(shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*sub[6]*sub[7])%(shp[6]/sub[6])*shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*sub[6])
                        +
                        dim[7]*(K/(sub[0]*sub[1]*sub[2]*sub[3]*sub[4]*sub[5]*sub[6])%sub[7]*shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*shp[6] + K/(shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*shp[6]*sub[7])%(shp[7]/sub[7])*shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*shp[6]*sub[7]);


                    inc = J/shp[0] * (sho[0]%sub[0])
                          + J/(shp[1] * shp[0]) * (sho[1]%sub[1])*sho[0]
                          + J/(shp[2] * shp[1] * shp[0]) * (sho[2]%sub[2]) * sho[0] * sho[1]
                          + J/(shp[3] * shp[2]*shp[1]*shp[0]) * (sho[3]%sub[3]) * sho[0]*sho[1]*sho[2]
                          + J/(shp[4] * shp[3]*shp[2]*shp[1]*shp[0]) * (sho[4]%sub[4]) * sho[0]*sho[1]*sho[2]*sho[3]
                          + J/(shp[5] * shp[4]*shp[3]*shp[2]*shp[1]*shp[0]) * (sho[5]%sub[5]) * sho[0]*sho[1]*sho[2]*sho[3]*sho[4]
                          + J/(shp[6] * shp[5]*shp[4]*shp[3]*shp[2]*shp[1]*shp[0]) * (sho[6]%sub[6]) * sho[0]*sho[1]*sho[2]*sho[3]*sho[4]*sho[5]
                          + J/(shp[7] * shp[6]*shp[5]*shp[4]*shp[3]*shp[2]*shp[1]*shp[0]) * (sho[7]%sub[7]) * sho[0]*sho[1]*sho[2]*sho[3]*sho[4]*sho[5]*sho[6];

                    memcpy(&dest[L * typesize], &src[(J + inc) * typesize], typesize);
                    K += 1;
                }
            }
            for (size_t L = K + cont; L < sho[0]*sho[1]*sho[2]*sho[3]*sho[4]*sho[5]*sho[6]*sho[7]; L++) {
                memcpy(&dest[L * typesize], &src[L * typesize], typesize);
            }
        }
        else {
            while (K < shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*shp[6]*shp[7]){

                if (((K + cont)%sho[0] >= sho[0] - sho[0]%sub[0])
                    || ((K + cont)%(sho[0]*sho[1])/(sho[0]) >= sho[1] - sho[1]%sub[1])
                    || ((K + cont)%(sho[0]*sho[1]*sho[2])/(sho[0]*sho[1]) >= sho[2] - sho[2]%sub[2])
                    || ((K + cont)%(sho[0]*sho[1]*sho[2]*sho[3])/(sho[0]*sho[1]*sho[2]) >= sho[3] - sho[3]%sub[3])
                    || ((K + cont)%(sho[0]*sho[1]*sho[2]*sho[3]*sho[4])/(sho[0]*sho[1]*sho[2]*sho[3]) >= sho[4] - sho[4]%sub[4])
                    || ((K + cont)%(sho[0]*sho[1]*sho[2]*sho[3]*sho[4]*sho[5])/(sho[0]*sho[1]*sho[2]*sho[3]*sho[4]) >= sho[5] - sho[5]%sub[5])
                    || ((K + cont)%(sho[0]*sho[1]*sho[2]*sho[3]*sho[4]*sho[5]*sho[6])/(sho[0]*sho[1]*sho[2]*sho[3]*sho[4]*sho[5]) >= sho[6] - sho[6]%sub[6])
                    || ((K + cont)%(sho[0]*sho[1]*sho[2]*sho[3]*sho[4]*sho[5]*sho[6]*sho[7])/(sho[0]*sho[1]*sho[2]*sho[3]*sho[4]*sho[5]*sho[6]) >= sho[7] - sho[7]%sub[7])){

                        memcpy(&dest[(K + cont) * typesize], &src[(K + cont) * typesize], typesize);
                        cont = cont + 1;

                } else {

                    L = K + cont;

                    J = dim[0]*((K)%sub[0] + K/(sub[0]*sub[1]*sub[2]*sub[3]*sub[4]*sub[5]*sub[6]*sub[7])%(shp[0]/sub[0])*sub[0])
                        +
                        dim[1]*(K/(sub[0])%sub[1]*shp[0] + K/(shp[0]*sub[1]*sub[2]*sub[3]*sub[4]*sub[5]*sub[6]*sub[7])%(shp[1]/sub[1])*shp[0]*sub[1])
                        +
                        dim[2]*(K/(sub[0]*sub[1])%sub[2]*shp[1]*shp[0] + K/(shp[0]*shp[1]*sub[2]*sub[3]*sub[4]*sub[5]*sub[6]*sub[7])%(shp[2]/sub[2])*shp[0]*shp[1]*sub[2])
                        +
                        dim[3]*(K/(sub[0]*sub[1]*sub[2])%sub[3]*shp[0]*shp[1]*shp[2] + K/(shp[0]*shp[1]*shp[2]*sub[3]*sub[4]*sub[5]*sub[6]*sub[7])%(shp[3]/sub[3])*shp[0]*shp[1]*shp[2]*sub[3])
                        +
                        dim[4]*(K/(sub[0]*sub[1]*sub[2]*sub[3])%sub[4]*shp[0]*shp[1]*shp[2]*shp[3] + K/(shp[0]*shp[1]*shp[2]*shp[3]*sub[4]*sub[5]*sub[6]*sub[7])%(shp[4]/sub[4])*shp[0]*shp[1]*shp[2]*shp[3]*sub[4])
                        +
                        dim[5]*(K/(sub[0]*sub[1]*sub[2]*sub[3]*sub[4])%sub[5]*shp[0]*shp[1]*shp[2]*shp[3]*shp[4] + K/(shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*sub[5]*sub[6]*sub[7])%(shp[5]/sub[5])*shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*sub[5])
                        +
                        dim[6]*(K/(sub[0]*sub[1]*sub[2]*sub[3]*sub[4]*sub[5])%sub[6]*shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5] + K/(shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*sub[6]*sub[7])%(shp[6]/sub[6])*shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*sub[6])
                        +
                        dim[7]*(K/(sub[0]*sub[1]*sub[2]*sub[3]*sub[4]*sub[5]*sub[6])%sub[7]*shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*shp[6] + K/(shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*shp[6]*sub[7])%(shp[7]/sub[7])*shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*shp[6]*sub[7]);

                    inc = J/shp[0] * (sho[0]%sub[0])
                          + J/(shp[1] * shp[0]) * (sho[1]%sub[1])*sho[0]
                          + J/(shp[2] * shp[1] * shp[0]) * (sho[2]%sub[2]) * sho[0] * sho[1]
                          + J/(shp[3] * shp[2]*shp[1]*shp[0]) * (sho[3]%sub[3]) * sho[0]*sho[1]*sho[2]
                          + J/(shp[4] * shp[3]*shp[2]*shp[1]*shp[0]) * (sho[4]%sub[4]) * sho[0]*sho[1]*sho[2]*sho[3]
                          + J/(shp[5] * shp[4]*shp[3]*shp[2]*shp[1]*shp[0]) * (sho[5]%sub[5]) * sho[0]*sho[1]*sho[2]*sho[3]*sho[4]
                          + J/(shp[6] * shp[5]*shp[4]*shp[3]*shp[2]*shp[1]*shp[0]) * (sho[6]%sub[6]) * sho[0]*sho[1]*sho[2]*sho[3]*sho[4]*sho[5]
                          + J/(shp[7] * shp[6]*shp[5]*shp[4]*shp[3]*shp[2]*shp[1]*shp[0]) * (sho[7]%sub[7]) * sho[0]*sho[1]*sho[2]*sho[3]*sho[4]*sho[5]*sho[6];

                    memcpy(&dest[(J + inc) * typesize], &src[L * typesize], typesize);
                    K += 1;
                }
            }
            for (size_t L = K + cont; L < sho[0]*sho[1]*sho[2]*sho[3]*sho[4]*sho[5]*sho[6]*sho[7]; L++) {
                memcpy(&dest[L * typesize], &src[L * typesize], typesize);
            }
        }
    }

    void tData_simple(char* src, char* dest, size_t typesize, size_t sub_shape[], size_t shape[], size_t dimension, size_t inverse) {

        size_t MAX_DIM = 8;
        size_t DIM = dimension;

        size_t dim[MAX_DIM], shp[MAX_DIM], sub[MAX_DIM];

        for (size_t i = 0; i < MAX_DIM; i++) {
            if (i < DIM) {
                dim[i] = 1;
                shp[DIM - i - 1] = shape[i];
                sub[DIM - i - 1] = sub_shape[i];
            } else {
                dim[i] = 0;
                shp[i] = 1;
                sub[i] = 1;
            }
        }

        size_t J;

        if (inverse == 0) {
            for (size_t K = 0; K < shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*shp[6]*shp[7]; K++) {

                J = dim[0]*((K)%sub[0] + K/(sub[0]*sub[1]*sub[2]*sub[3]*sub[4]*sub[5]*sub[6]*sub[7])%(shp[0]/sub[0])*sub[0])
                    +
                    dim[1]*(K/(sub[0])%sub[1]*shp[0] + K/(shp[0]*sub[1]*sub[2]*sub[3]*sub[4]*sub[5]*sub[6]*sub[7])%(shp[1]/sub[1])*shp[0]*sub[1])
                    +
                    dim[2]*(K/(sub[0]*sub[1])%sub[2]*shp[1]*shp[0] + K/(shp[0]*shp[1]*sub[2]*sub[3]*sub[4]*sub[5]*sub[6]*sub[7])%(shp[2]/sub[2])*shp[0]*shp[1]*sub[2])
                    +
                    dim[3]*(K/(sub[0]*sub[1]*sub[2])%sub[3]*shp[0]*shp[1]*shp[2] + K/(shp[0]*shp[1]*shp[2]*sub[3]*sub[4]*sub[5]*sub[6]*sub[7])%(shp[3]/sub[3])*shp[0]*shp[1]*shp[2]*sub[3])
                    +
                    dim[4]*(K/(sub[0]*sub[1]*sub[2]*sub[3])%sub[4]*shp[0]*shp[1]*shp[2]*shp[3] + K/(shp[0]*shp[1]*shp[2]*shp[3]*sub[4]*sub[5]*sub[6]*sub[7])%(shp[4]/sub[4])*shp[0]*shp[1]*shp[2]*shp[3]*sub[4])
                    +
                    dim[5]*(K/(sub[0]*sub[1]*sub[2]*sub[3]*sub[4])%sub[5]*shp[0]*shp[1]*shp[2]*shp[3]*shp[4] + K/(shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*sub[5]*sub[6]*sub[7])%(shp[5]/sub[5])*shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*sub[5])
                    +
                    dim[6]*(K/(sub[0]*sub[1]*sub[2]*sub[3]*sub[4]*sub[5])%sub[6]*shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5] + K/(shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*sub[6]*sub[7])%(shp[6]/sub[6])*shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*sub[6])
                    +
                    dim[7]*(K/(sub[0]*sub[1]*sub[2]*sub[3]*sub[4]*sub[5]*sub[6])%sub[7]*shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*shp[6] + K/(shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*shp[6]*sub[7])%(shp[7]/sub[7])*shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*shp[6]*sub[7]);


                memcpy(&dest[K * typesize], &src[J * typesize], typesize);
            }
        } else {
            for (size_t K = 0; K < shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*shp[6]*shp[7]; K++) {

                J = dim[0]*((K)%sub[0] + K/(sub[0]*sub[1]*sub[2]*sub[3]*sub[4]*sub[5]*sub[6]*sub[7])%(shp[0]/sub[0])*sub[0])
                    +
                    dim[1]*(K/(sub[0])%sub[1]*shp[0] + K/(shp[0]*sub[1]*sub[2]*sub[3]*sub[4]*sub[5]*sub[6]*sub[7])%(shp[1]/sub[1])*shp[0]*sub[1])
                    +
                    dim[2]*(K/(sub[0]*sub[1])%sub[2]*shp[1]*shp[0] + K/(shp[0]*shp[1]*sub[2]*sub[3]*sub[4]*sub[5]*sub[6]*sub[7])%(shp[2]/sub[2])*shp[0]*shp[1]*sub[2])
                    +
                    dim[3]*(K/(sub[0]*sub[1]*sub[2])%sub[3]*shp[0]*shp[1]*shp[2] + K/(shp[0]*shp[1]*shp[2]*sub[3]*sub[4]*sub[5]*sub[6]*sub[7])%(shp[3]/sub[3])*shp[0]*shp[1]*shp[2]*sub[3])
                    +
                    dim[4]*(K/(sub[0]*sub[1]*sub[2]*sub[3])%sub[4]*shp[0]*shp[1]*shp[2]*shp[3] + K/(shp[0]*shp[1]*shp[2]*shp[3]*sub[4]*sub[5]*sub[6]*sub[7])%(shp[4]/sub[4])*shp[0]*shp[1]*shp[2]*shp[3]*sub[4])
                    +
                    dim[5]*(K/(sub[0]*sub[1]*sub[2]*sub[3]*sub[4])%sub[5]*shp[0]*shp[1]*shp[2]*shp[3]*shp[4] + K/(shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*sub[5]*sub[6]*sub[7])%(shp[5]/sub[5])*shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*sub[5])
                    +
                    dim[6]*(K/(sub[0]*sub[1]*sub[2]*sub[3]*sub[4]*sub[5])%sub[6]*shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5] + K/(shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*sub[6]*sub[7])%(shp[6]/sub[6])*shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*sub[6])
                    +
                    dim[7]*(K/(sub[0]*sub[1]*sub[2]*sub[3]*sub[4]*sub[5]*sub[6])%sub[7]*shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*shp[6] + K/(shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*shp[6]*sub[7])%(shp[7]/sub[7])*shp[0]*shp[1]*shp[2]*shp[3]*shp[4]*shp[5]*shp[6]*sub[7]);

                memcpy(&dest[J * typesize], &src[K * typesize], typesize);
            }
        }
    }

    int tData(char* src, char* dest, size_t typesize, size_t sub_shape[], size_t shape[], size_t dimension, size_t inverse) {
        size_t DIM = dimension;
        for (size_t i = 0; i < DIM; i++) {
            if (shape[i]%sub_shape[i] != 0){
                tData_general(src, dest, typesize, sub_shape, shape, dimension, inverse);
                return 0;
            }
        }

        tData_simple(src, dest, typesize, sub_shape, shape, dimension, inverse);
        return 1;
    }

    ''', libraries=[])

ffibuilder.cdef(
    '''
    void tData(char* src, char* dest, size_t typesize, size_t sub_shape[], size_t shape[], size_t dimension, size_t inverse);
    void tData_general(char* src, char* dest, size_t typesize, size_t sub_shape[], size_t shape[], size_t dimension, size_t inverse);
    void tData_simple(char* src, char* dest, size_t typesize, size_t sub_shape[], size_t shape[], size_t dimension, size_t inverse);

    ''')

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)