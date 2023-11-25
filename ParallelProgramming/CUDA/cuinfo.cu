/*Theocharis_Kazakidis_4679*/
#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>

/* 
 * Retrieves and prints information for every installed NVIDIA
 * GPU device
 */
void cuinfo_print_devinfo()
{
	int num_devs, i;
	cudaDeviceProp dev_prop;
	
	cudaGetDeviceCount(&num_devs);
	if (num_devs == 0)
	{
		printf("No CUDA devices found.\n");
		return;
	}
	
	for (i = 0; i < num_devs; i++)
	{
        cudaGetDeviceProperties(&dev_prop, i);

        printf(" ID Συσκευής: %d\n", i);
        printf(" Όνομα Συσκευής: %s\n", dev_prop.name);
        printf(" Υπολογισμός Ικανότητας CUDA: %d.%d\n", dev_prop.major, dev_prop.minor);
        printf(" Πλήθος SMs: %d\n", dev_prop.multiProcessorCount);
        printf(" Μέγιστο Πλήθος Νημάτων Ανά Μπλοκ: %d\n", dev_prop.maxThreadsPerBlock);
        printf(" Συνολική Global Μνήμη: %f GB\n", dev_prop.totalGlobalMem / (1024.0 * 1024.0 * 1024.0));
        printf(" Συνολική Shared Μνήμη Ανά Μπλοκ: %f MB\n", dev_prop.sharedMemPerBlock / (1024.0 * 1024.0));
        printf(" Εκτιμόμενο Συνολικό Πλήθος Πυρήνων: %d\n",dev_prop.multiProcessorCount * dev_prop.maxThreadsPerMultiProcessor * dev_prop.warpSize);
	}
}

int main()
{
	cuinfo_print_devinfo();
	return 0;
}
