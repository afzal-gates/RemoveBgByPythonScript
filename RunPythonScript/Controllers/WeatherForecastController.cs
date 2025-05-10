using Microsoft.AspNetCore.Mvc;
using Python.Runtime;

namespace RunPythonScript.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class WeatherForecastController : ControllerBase
    {
        private static readonly string[] Summaries = new[]
        {
            "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
        };

        private readonly ILogger<WeatherForecastController> _logger;
        public WeatherForecastController(ILogger<WeatherForecastController> logger)
        {
            _logger = logger;
        }

        [HttpGet]
        public IEnumerable<WeatherForecast> Get()
        {
            return Enumerable.Range(1, 5).Select(index => new WeatherForecast
            {
                Date = DateOnly.FromDateTime(DateTime.Now.AddDays(index)),
                TemperatureC = Random.Shared.Next(-20, 55),
                Summary = Summaries[Random.Shared.Next(Summaries.Length)]
            })
            .ToArray();
        }


        [HttpGet("python")]
        public async Task<IActionResult> GetPython()
        {
            try
            {
                var result = RunPythonScript("AnimationGenAI").Result;
                return Ok((string)result+"="+Guid.NewGuid());
            }
            catch(Exception ex)
            {
                return BadRequest();
            }
        }

        private async Task<string> RunPythonScript(string scriptName)
        {
            if (!PythonEngine.IsInitialized)
            {
                //PythonEngine.Shutdown();
                Runtime.PythonDLL = @"C:\Python312\python312.dll";

                PythonEngine.Initialize(); 
                PythonEngine.BeginAllowThreads();
            }
            try
            {
                dynamic result;
                using (Py.GIL())
                {
                    dynamic sys = Py.Import("sys");
                    sys.path.append(@"C:\Users\localadmin\source\repos\RunPythonScript\RunPythonScript\");
                    var pythonScript = Py.Import(scriptName);

                    result = pythonScript.InvokeMethod("");
                    Console.WriteLine(result);
                }
                return result;
            }
            catch(Exception ex)
            {
                Console.WriteLine(ex);
                throw;
            }
        }
    }
}
