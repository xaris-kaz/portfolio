#include <stdio.h>
#include <omp.h>

#define UPTO 10000000

long int count,      /* number of primes */ 
         lastprime;  /* the last prime found */

double begin_serial=0, finish_serial=0,begin_parallel=0, finish_parallel=0;

void serial_primes(long int n) {
	long int i, num, divisor, quotient, remainder;

	if (n < 2) return;
	count = 1;                         /* 2 is the first prime */
	lastprime = 2;

	begin_serial=omp_get_wtime();

	for (i = 0; i < (n-1)/2; ++i) {    /* For every odd number */
		num = 2*i + 3;

		divisor = 1;
		do 
		{
			divisor += 2;                  /* Divide by the next odd */
			quotient  = num / divisor;  
			remainder = num % divisor;  
		} while (remainder && divisor <= quotient);  /* Don't go past sqrt */

		if (remainder || divisor == num) /* num is prime */
		{
			count++;
			lastprime = num;
		}
	}

	finish_serial=omp_get_wtime();
}


void openmp_primes(long int n) {
	long int i, num, divisor, quotient, remainder;

	if (n < 2) return;
	count = 1;                         /* 2 is the first prime */
	lastprime = 2;

	begin_parallel=omp_get_wtime();
	//#pragma omp parallel for shared(i) private(num, divisor, quotient, remainder) reduction(+: count) num_threads(3) schedule(static) 
	#pragma omp parallel for shared(i) private(num, divisor, quotient, remainder) reduction(+: count) num_threads(1) schedule(dynamic) 
	//#pragma omp parallel for shared(i) private(num, divisor, quotient, remainder) reduction(+: count) num_threads(3) schedule(static) 
//dynamic, guided
	for (i = 0; i < (n-1)/2; ++i) {    /* For every odd number */
		num = 2*i + 3;

		divisor = 1;
		do 
		{
			divisor += 2;                  /* Divide by the next odd */
			quotient  = num / divisor;  
			remainder = num % divisor;  
		} while (remainder && divisor <= quotient);  /* Don't go past sqrt */

		if (remainder || divisor == num) /* num is prime */
		{
			count++;
			#pragma opm critical
			lastprime = num;
		}
	}
	finish_parallel=omp_get_wtime();
}


int main()
{
	printf("Serial and parallel prime number calculations:\n\n");
	
	/* Time the following to compare performance 
	 */
	serial_primes(UPTO);        /* time it */
	printf("[serial] count = %ld, last = %ld (time = %f)\n", count, lastprime, (finish_serial-begin_serial));
	openmp_primes(UPTO);        /* time it */
	printf("[openmp] count = %ld, last = %ld (time = %f)\n", count, lastprime, (finish_parallel-begin_parallel));
	
	return 0;
}
