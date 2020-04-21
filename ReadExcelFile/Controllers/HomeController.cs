using OfficeOpenXml;
using PyRunner;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Web;
using System.Web.Mvc;

namespace ReadExcelFile.Controllers
{
    public class HomeController : Controller
    {
        public ActionResult Index()
        {
            return View();
        }

        [HttpPost]
        public ActionResult Uploads()
        {
            var pythonPath = ConfigurationManager.AppSettings["pythonPath"];
            PythonRunner pythonRunner = new PythonRunner(pythonPath, 2000000);
            var uploadRootFolderInput = AppDomain.CurrentDomain.BaseDirectory + "PythonScripts";
            var uploadFolder = AppDomain.CurrentDomain.BaseDirectory + "Uploads";
            DeleteFiles(uploadFolder);

            string cScript = uploadRootFolderInput + "\\plot_stock_market.py";
            
            string returnValue = pythonRunner.Execute(cScript, uploadFolder);

            var result = Regex.Split(returnValue, "\r\n|\r|\n");
            List<string> data = new List<string>();
            foreach (var item in result)
            {
                data.Add(item);
            }

            ////Get Image data
            //PythonRunner p = new PythonRunner(pythonPath, 2000000);
            //string iScript = uploadRootFolderInput + "\\plot_stock_market.py";
            //byte[] d = ImageToByte2(pythonRunner.GetImage(iScript));
            //if (d != null)
            //{
            //    ViewBag.Base64String = "data:image/png;base64," + Convert.ToBase64String(d, 0, d.Length);
            //}

            //if (Request.Files.Count > 0)
            //{
            //    try
            //    {
            //        HttpFileCollectionBase files = Request.Files;
            //        for (int i = 0; i < files.Count; i++)
            //        {
            //            HttpPostedFileBase file = files[i];
            //            string fname;
            //            if (Request.Browser.Browser.ToUpper() == "IE" || Request.Browser.Browser.ToUpper() == "INTERNETEXPLORER")
            //            {
            //                string[] testfiles = file.FileName.Split(new char[] { '\\' });
            //                fname = testfiles[testfiles.Length - 1];
            //            }
            //            else
            //            {
            //                fname = file.FileName;
            //            }
            //            var newName = fname.Split('.');
            //            fname = newName[0] + "_" + DateTime.Now.Ticks.ToString() + "." + newName[1];
            //            var uploadRootFolderInput = AppDomain.CurrentDomain.BaseDirectory + "\\Uploads";
            //            Directory.CreateDirectory(uploadRootFolderInput);
            //            var directoryFullPathInput = uploadRootFolderInput;
            //            fname = Path.Combine(directoryFullPathInput, fname);
            //            file.SaveAs(fname);
            //            excelData = readXLS(fname);
            //        }
            //        return Json(excelData);
            //    }
            //    catch (Exception ex)
            //    {
            //        return Json(excelData);
            //    }
            //}
            //else
            //{
            //    return Json(excelData);
            //}

            return Json(data);
        }

        private void DeleteFiles(string uploadFolder)
        {
            System.IO.DirectoryInfo di = new DirectoryInfo(uploadFolder);

            foreach (FileInfo file in di.GetFiles())
            {
                file.Delete();
            }
            foreach (DirectoryInfo dir in di.GetDirectories())
            {
                dir.Delete(true);
            }
        }


        public List<ExcelData> readXLS(string FilePath)
        {
            List<ExcelData> excelData = new List<ExcelData>();
            FileInfo existingFile = new FileInfo(FilePath);
            using (ExcelPackage package = new ExcelPackage(existingFile))
            {
                ExcelWorksheet worksheet = package.Workbook.Worksheets[1];
                int rowCount = worksheet.Dimension.End.Row;
                for (int row = 2; row <= rowCount; row++)
                {
                    excelData.Add(new ExcelData()
                    {
                        Date = worksheet.Cells[row, 1].Value.ToString().Trim(),
                        Task = worksheet.Cells[row, 2].Value.ToString().Trim(),
                        Time = worksheet.Cells[row, 3].Value.ToString().Trim()
                    });
                }
            }
            return excelData;
        }

        public byte[] ImageToByte2(Bitmap img)
        {
            using (var stream = new MemoryStream())
            {
                img.Save(stream, System.Drawing.Imaging.ImageFormat.Bmp);
                return stream.ToArray();
            }
        }

    }
    public class ExcelData
    {
        public string Date { get; set; }
        public string Task { get; set; }
        public string Time { get; set; }
    }
}