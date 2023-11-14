using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading.Tasks;

namespace Test
{
    class Program
    {
        public string ReturnsString(int num)
        {
            if (num > 0)
            {
                return "hello world.";
            }
            else
            {
                return "goodbye world.";
            }
        }
    }
}
