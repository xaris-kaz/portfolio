#include <stdio.h>
#include <omp.h>

int main()
{
int i, sum = 0;

#pragma omp parallel
#pragma omp taskloop private(i) reduction(+:sum)
for (i = 0; i < 100; i++) {
sum += i;
}

printf("sum = %d\n", sum);
return 0;
}

