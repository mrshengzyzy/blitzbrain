package main

import (
	"bufio"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"strings"
)

func main() {

	pwd := "D:\\04MySpace\\phecda\\icons\\"
	filename := "check.svg"
	file, writer := prepareWriter(pwd, filename)
	defer file.Close()
	err := writeHeader(writer)
	if err != nil {
		panic(err)
	}

	// 合并 SVG
	files, _ := listFiles(fmt.Sprintf("%s\\svgs", pwd), "svg")
	for _, f := range files {
		fmt.Printf("start merge: %s\n", f)
		err = writeTemplate(writer, f, findId(f))
		if err != nil {
			panic(err)
		}
	}

	err = writeDefs(writer)
	if err != nil {
		panic(err)
	}

	// 显示合并的 SVG
	for index, f := range files {
		fmt.Printf("display svg: %s\n", f)
		err = writePosition(writer, findId(f), index)
		if err != nil {
			panic(err)
		}
	}

	err = writeTail(writer)
	if err != nil {
		panic(err)
	}

	fmt.Printf("=========== check file target: %s\n", file.Name())
}

func prepareWriter(pwd, filename string) (*os.File, *bufio.Writer) {
	file, err := os.OpenFile(fmt.Sprintf("%s%s", pwd, filename), os.O_CREATE|os.O_RDWR|os.O_TRUNC, 0666)
	if err != nil {
		panic(err)
	}
	return file, bufio.NewWriter(file)
}

func writeHeader(writer *bufio.Writer) (err error) {
	header := "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<svg version=\"2.0\" xmlns=\"http://www.w3.org/2000/svg\" height=\"600\" width=\"1000\">\n<rect width=\"100%\" height=\"100%\" fill=\"white\" />\n<defs>\n"
	_, err = writer.WriteString(header)
	return
}

func writeDefs(writer *bufio.Writer) (err error) {
	_, err = writer.WriteString("</defs>\n")
	_ = writer.Flush()
	return
}

func writeTemplate(writer *bufio.Writer, filename, id string) (err error) {
	file, err := os.Open(filename)
	if err != nil {
		return
	}
	defer file.Close()
	reader := bufio.NewReader(file)
	for {
		line, err := reader.ReadString('\n')
		if err != nil || io.EOF == err {
			if len(line) == 0 {
				break
			}
		}

		if line == "</svg>" {
			_, _ = writer.WriteString("</g>\n")
		} else if strings.HasPrefix(line, "<svg") {
			_, _ = writer.WriteString("<g id=\"" + id + "\" transform=\"scale(5)\">\n")
		} else {
			_, _ = writer.WriteString(line)
		}
	}
	_ = writer.Flush()
	return
}

func writePosition(writer *bufio.Writer, id string, index int) (err error) {
	// 20 个图标一行
	line := index / 20
	column := index % 20

	// 计算行列坐标(因原点从左上角开始,所以 x y 正好相反)
	x := column * 100
	y := line*100 + 10

	template := fmt.Sprintf("<g transform=\"scale(0.5) translate(%d %d)\">\n <use href=\"#%s\"/>\n</g>\n", x, y, id)
	_, err = writer.WriteString(template)
	_ = writer.Flush()
	return
}

func writeTail(writer *bufio.Writer) (err error) {
	_, err = writer.WriteString("</svg>")
	_ = writer.Flush()
	return
}

func findId(filename string) string {
	arr := strings.Split(filename, "\\")
	pureName := arr[len(arr)-1]
	return strings.Split(pureName, ".")[0]
}

func listFiles(dirPth string, suffix string) (files []string, err error) {
	files = make([]string, 0, 10)
	dir, err := ioutil.ReadDir(dirPth)
	if err != nil {
		return nil, err
	}
	PthSep := string(os.PathSeparator)
	suffix = strings.ToUpper(suffix) //忽略后缀匹配的大小写
	for _, fi := range dir {
		if fi.IsDir() { // 忽略目录
			continue
		}
		if strings.HasSuffix(strings.ToUpper(fi.Name()), suffix) { //匹配文件
			files = append(files, dirPth+PthSep+fi.Name())
		}
	}
	return files, nil
}
