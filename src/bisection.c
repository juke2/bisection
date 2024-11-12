#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

typedef double (*func)(double);

char f_ex_str[] = "FE_x";
char f_x_str[] = "F_x";
char g_x_str[] = "G_x";
char h_x_str[] = "H_x";
char v_x_str[] = "V_x";

double bisection(double (*function)(double), double a, double b, int maxiter, double ftol)
{
    double x_r, f_a, f_x_r;
    // printf("%1.50f = ftol\n \n", ftol);
    for (int iter = 0; iter < maxiter; iter++)
    {
        x_r = (a + b) / 2.0;
        f_a = (*function)(a);
        // printf("%1.50f \n \n", f_a);
        f_x_r = (*function)(x_r);
        // printf("%1.50f \n \n", f_x_r);

        if (fabs(f_x_r) < ftol)
        {
            return x_r;
        }
        if (f_a * f_x_r < 0)
        {
            b = x_r;
        }
        else
        {
            a = x_r;
        }
    }
    return NAN;
}

double f_ex(double x)
{
    return pow((x - sqrt(2.0)), 3.0);
}
double f_x(double x)
{
    return (1.0 - x) * sin(exp(-pow(x, 2.0))) - x * cos(0.5 * pow(x, 2.0));
}
double g_x(double x)
{
    return (pow(x, 2.0) - 7.0 / 2.0 * x - 15.0 / 2.0) * ((8.0 * pow(x, 2.0) - 10.0 * x - 3.0) / 100.0);
}
double h_x(double x)
{
    return sin(M_PI * x) + sin(2 * M_PI * x) + sin(3 * M_PI * x);
}
double v_x(double x)
{
    return h_x(x) - g_x(x);
}
double dummy_function(double x)
{
    return 0;
}

func function_decider(char input_string[])
{
    // printf("%s == %s : %d \n \n ", input_string, f_ex_str, strcmp(input_string, f_ex_str));
    // printf("len(input) == len(f_ex_str) : %d == %d \n\n", strlen(input_string), strlen(f_ex_str));
    if (strcmp(input_string, f_ex_str) == 0)
    {
        return (func)&f_ex;
    }
    else if (strcmp(input_string, f_x_str) == 0)
    {
        return (func)&f_x;
    }
    else if (strcmp(input_string, g_x_str) == 0)
    {
        return (func)&g_x;
    }
    else if (strcmp(input_string, h_x_str) == 0)
    {
        return (func)&h_x;
    }
    else if (strcmp(input_string, v_x_str) == 0)
    {
        return (func)&v_x;
    }
    printf("Comparison failed if you are seeing this \n\n\n");
    return (func)&dummy_function;
}
int main(int argc, char **argv)
{
    func function;
    char **__restrict eptr;
    double a, b, ftol, result;
    int maxiter;
    if (argc == 6)
    {
        // printf("%s %s %s %s %s \n", argv[1], argv[2], argv[3], argv[4], argv[5]);
        function = function_decider(argv[1]);
        a = strtod(argv[2], eptr);
        b = strtod(argv[3], eptr);
        maxiter = atoi(argv[4]);
        ftol = strtod(argv[5], eptr);
        // printf("%f %f %d %1.20f", a, b, maxiter, ftol);
        result = bisection(function, a, b, maxiter, ftol);
        printf("%f", result);
        FILE *file_pointer;
        file_pointer = fopen("src/output/output_c.txt", "w");
        fprintf(file_pointer, "%.30f", result);
        fclose(file_pointer);
    }
    else
    {
        printf("Invalid amount of arguments. (6 expected, %.d recieved).", argc);
    }
    return 0;
}
