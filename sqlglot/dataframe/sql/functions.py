from __future__ import annotations

import typing as t
from inspect import signature

from sqlglot import expressions as glotexp
from sqlglot.dataframe.sql.column import Column
from sqlglot.helper import flatten as _flatten

if t.TYPE_CHECKING:
    from sqlglot.dataframe.sql._typing import ColumnOrName, ColumnOrPrimitive
    from sqlglot.dataframe.sql.dataframe import DataFrame


def col(column_name: t.Union[ColumnOrName, t.Any]) -> Column:
    return Column(column_name)


def lit(value: t.Optional[t.Any] = None) -> Column:
    if isinstance(value, str):
        return Column(glotexp.Literal(this=str(value), is_string=True))
    return Column(value)


def greatest(*cols: ColumnOrName) -> Column:
    cols = [Column.ensure_col(col) for col in cols]
    return Column.invoke_expression_over_column(
        cols[0], glotexp.Greatest, expressions=[col.expression for col in cols[1:]] if len(cols) > 1 else None
    )


def least(*cols: ColumnOrName) -> Column:
    cols = [Column.ensure_col(col) for col in cols]
    return Column.invoke_expression_over_column(
        cols[0], glotexp.Least, expressions=[col.expression for col in cols[1:]] if len(cols) > 1 else None
    )


def count_distinct(col: ColumnOrName, *cols: ColumnOrName) -> Column:
    cols = [Column.ensure_col(x) for x in [col] + list(cols)]
    if len(cols) > 1:
        raise NotImplementedError("Multiple columns in a count distinct is not supported")
    return Column(glotexp.Count(this=glotexp.Distinct(this=cols[0].expression)))


def countDistinct(col: ColumnOrName, *cols: ColumnOrName) -> Column:
    return count_distinct(col, *cols)


def when(condition: Column, value: t.Any) -> Column:
    true_value = value if isinstance(value, Column) else lit(value)
    return Column(glotexp.Case(ifs=[glotexp.If(this=condition.column_expression, true=true_value.column_expression)]))


def asc(col: ColumnOrName) -> Column:
    return Column.ensure_col(col).asc()


def desc(col: ColumnOrName):
    return Column.ensure_col(col).desc()


def broadcast(df: DataFrame) -> DataFrame:
    return df.hint("broadcast")


def sqrt(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.Sqrt)


def abs(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.Abs)


def max(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.Max)


def min(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.Min)


def max_by(col: ColumnOrName, ord: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "MAX_BY", ord)


def min_by(col: ColumnOrName, ord: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "MIN_BY", ord)


def count(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.Count)


def sum(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.Sum)


def avg(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.Avg)


def mean(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "MEAN")


def sumDistinct(col: ColumnOrName) -> Column:
    return sum_distinct(col)


def sum_distinct(col: ColumnOrName) -> Column:
    raise NotImplementedError("Sum distinct is not currently implemented")


def product(col: ColumnOrName) -> Column:
    raise NotImplementedError("Product is not currently implemented")


def acos(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "ACOS")


def acosh(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "ACOSH")


def asin(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "ASIN")


def asinh(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "ASINH")


def atan(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "ATAN")


def atan2(col1: t.Union[ColumnOrName, float], col2: t.Union[ColumnOrName, float]) -> Column:
    return Column.invoke_anonymous_function(col1, "ATAN2", col2)


def atanh(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "ATANH")


def cbrt(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "CBRT")


def ceil(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.Ceil)


def cos(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "COS")


def cosh(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "COSH")


def cot(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "COT")


def csc(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "CSC")


def exp(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "EXP")


def expm1(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "EXPM1")


def floor(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.Floor)


def log10(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.Log10)


def log1p(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "LOG1P")


def log2(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.Log2)


def log(arg1: t.Union[ColumnOrName, float], arg2: t.Optional[ColumnOrName] = None) -> Column:
    if arg2 is None:
        return Column.invoke_expression_over_column(arg1, glotexp.Ln)
    return Column.invoke_expression_over_column(arg1, glotexp.Log, expression=Column.ensure_col(arg2).expression)


def rint(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "RINT")


def sec(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "SEC")


def signum(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "SIGNUM")


def sin(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "SIN")


def sinh(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "SINH")


def tan(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "TAN")


def tanh(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "TANH")


def toDegrees(col: ColumnOrName) -> Column:
    return degrees(col)


def degrees(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "DEGREES")


def toRadians(col: ColumnOrName) -> Column:
    return radians(col)


def radians(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "RADIANS")


def bitwiseNOT(col: ColumnOrName) -> Column:
    return bitwise_not(col)


def bitwise_not(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.BitwiseNot)


def asc_nulls_first(col: ColumnOrName) -> Column:
    return Column.ensure_col(col).asc_nulls_first()


def asc_nulls_last(col: ColumnOrName) -> Column:
    return Column.ensure_col(col).asc_nulls_last()


def desc_nulls_first(col: ColumnOrName) -> Column:
    return Column.ensure_col(col).desc_nulls_first()


def desc_nulls_last(col: ColumnOrName) -> Column:
    return Column.ensure_col(col).desc_nulls_last()


def stddev(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.Stddev)


def stddev_samp(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.StddevSamp)


def stddev_pop(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.StddevPop)


def variance(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.Variance)


def var_samp(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.Variance)


def var_pop(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.VariancePop)


def skewness(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "SKEWNESS")


def kurtosis(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "KURTOSIS")


def collect_list(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "COLLECT_LIST")


def collect_set(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "COLLECT_SET")


def hypot(col1: t.Union[ColumnOrName, float], col2: t.Union[ColumnOrName, float]) -> Column:
    return Column.invoke_anonymous_function(col1, "HYPOT", col2)


def pow(col1: t.Union[ColumnOrName, float], col2: t.Union[ColumnOrName, float]) -> Column:
    return Column.invoke_anonymous_function(col1, "POW", col2)


def row_number() -> Column:
    return Column(glotexp.Anonymous(this="ROW_NUMBER"))


def dense_rank() -> Column:
    return Column(glotexp.Anonymous(this="DENSE_RANK"))


def rank() -> Column:
    return Column(glotexp.Anonymous(this="RANK"))


def cume_dist() -> Column:
    return Column(glotexp.Anonymous(this="CUME_DIST"))


def percent_rank() -> Column:
    return Column(glotexp.Anonymous(this="PERCENT_RANK"))


def approxCountDistinct(col: ColumnOrName, rsd: t.Optional[float] = None) -> Column:
    return approx_count_distinct(col, rsd)


def approx_count_distinct(col: ColumnOrName, rsd: t.Optional[float] = None) -> Column:
    if rsd is None:
        return Column.invoke_expression_over_column(col, glotexp.ApproxDistinct)
    return Column.invoke_expression_over_column(col, glotexp.ApproxDistinct, accuracy=Column.ensure_col(rsd).expression)


def coalesce(*cols: ColumnOrName) -> Column:
    cols = [Column.ensure_col(col) for col in cols]
    return Column.invoke_expression_over_column(
        cols[0], glotexp.Coalesce, expressions=[col.expression for col in cols[1:]] if len(cols) > 1 else None
    )


def corr(col1: ColumnOrName, col2: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col1, "CORR", col2)


def covar_pop(col1: ColumnOrName, col2: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col1, "COVAR_POP", col2)


def covar_samp(col1: ColumnOrName, col2: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col1, "COVAR_SAMP", col2)


def first(col: ColumnOrName, ignorenulls: bool = None) -> Column:
    if ignorenulls is not None:
        return Column.invoke_anonymous_function(col, "FIRST", ignorenulls)
    return Column.invoke_anonymous_function(col, "FIRST")


def grouping_id(*cols: ColumnOrName) -> Column:
    if len(cols) == 0:
        return Column.invoke_anonymous_function(None, "GROUPING_ID")
    if len(cols) == 1:
        return Column.invoke_anonymous_function(cols[0], "GROUPING_ID")
    return Column.invoke_anonymous_function(cols[0], "GROUPING_ID", *cols[1:])


def input_file_name() -> Column:
    return Column.invoke_anonymous_function(None, "INPUT_FILE_NAME")


def isnan(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "ISNAN")


def isnull(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "ISNULL")


def last(col: ColumnOrName, ignorenulls: bool = None) -> Column:
    if ignorenulls is not None:
        return Column.invoke_anonymous_function(col, "LAST", ignorenulls)
    return Column.invoke_anonymous_function(col, "LAST")


def monotonically_increasing_id() -> Column:
    return Column.invoke_anonymous_function(None, "MONOTONICALLY_INCREASING_ID")


def nanvl(col1: ColumnOrName, col2: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col1, "NANVL", col2)


def percentile_approx(
    col: ColumnOrName,
    percentage: t.Union[ColumnOrName, float, t.List[float], t.Tuple[float]],
    accuracy: t.Union[ColumnOrName, float] = None,
) -> Column:
    if accuracy:
        return Column.invoke_anonymous_function(col, "PERCENTILE_APPROX", percentage, accuracy)
    return Column.invoke_anonymous_function(col, "PERCENTILE_APPROX", percentage)


def rand(seed: ColumnOrPrimitive = None) -> Column:
    return Column.invoke_anonymous_function(seed, "RAND")


def randn(seed: ColumnOrPrimitive = None) -> Column:
    return Column.invoke_anonymous_function(seed, "RANDN")


def round(col: ColumnOrName, scale: int = None) -> Column:
    if scale is not None:
        return Column.invoke_anonymous_function(col, "ROUND", scale)
    return Column.invoke_anonymous_function(col, "ROUND")


def bround(col: ColumnOrName, scale: int = None) -> Column:
    if scale is not None:
        return Column.invoke_anonymous_function(col, "BROUND", scale)
    return Column.invoke_anonymous_function(col, "BROUND")


def shiftleft(col: ColumnOrName, numBits: int) -> Column:
    return Column.invoke_expression_over_column(
        col, glotexp.BitwiseLeftShift, expression=Column.ensure_col(numBits).expression
    )


def shiftLeft(col: ColumnOrName, numBits: int) -> Column:
    return shiftleft(col, numBits)


def shiftright(col: ColumnOrName, numBits: int) -> Column:
    return Column.invoke_expression_over_column(
        col, glotexp.BitwiseRightShift, expression=Column.ensure_col(numBits).expression
    )


def shiftRight(col: ColumnOrName, numBits: int) -> Column:
    return shiftright(col, numBits)


def shiftrightunsigned(col: ColumnOrName, numBits: int) -> Column:
    return Column.invoke_anonymous_function(col, "SHIFTRIGHTUNSIGNED", numBits)


def shiftRightUnsigned(col: ColumnOrName, numBits: int) -> Column:
    return shiftrightunsigned(col, numBits)


def expr(str: str) -> Column:
    return Column(str)


def struct(col: t.Union[ColumnOrName, t.Iterable[ColumnOrName]], *cols: ColumnOrName) -> Column:
    col = [col] if isinstance(col, (str, Column)) else col
    columns = col + list(cols)
    expressions = [Column.ensure_col(column).expression for column in columns]
    return Column(glotexp.Struct(expressions=expressions))


def conv(col: ColumnOrName, fromBase: int, toBase: int) -> Column:
    return Column.invoke_anonymous_function(col, "CONV", fromBase, toBase)


def factorial(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "FACTORIAL")


def lag(col: ColumnOrName, offset: t.Optional[int] = 1, default: t.Optional[t.Any] = None) -> Column:
    if default is not None:
        return Column.invoke_anonymous_function(col, "LAG", offset, default)
    if offset != 1:
        return Column.invoke_anonymous_function(col, "LAG", offset)
    return Column.invoke_anonymous_function(col, "LAG")


def lead(col: ColumnOrName, offset: t.Optional[int] = 1, default: t.Optional[t.Any] = None) -> Column:
    if default is not None:
        return Column.invoke_anonymous_function(col, "LEAD", offset, default)
    if offset != 1:
        return Column.invoke_anonymous_function(col, "LEAD", offset)
    return Column.invoke_anonymous_function(col, "LEAD")


def nth_value(col: ColumnOrName, offset: t.Optional[int] = 1, ignoreNulls: t.Optional[bool] = None) -> Column:
    if ignoreNulls is not None:
        raise NotImplementedError("There is currently not support for `ignoreNulls` parameter")
    if offset != 1:
        return Column.invoke_anonymous_function(col, "NTH_VALUE", offset)
    return Column.invoke_anonymous_function(col, "NTH_VALUE")


def ntile(n: int) -> Column:
    return Column.invoke_anonymous_function(None, "NTILE", n)


def current_date() -> Column:
    return Column.invoke_expression_over_column(None, glotexp.CurrentDate)


def current_timestamp() -> Column:
    return Column.invoke_expression_over_column(None, glotexp.CurrentTimestamp)


def date_format(col: ColumnOrName, format: str) -> Column:
    return Column.invoke_anonymous_function(col, "DATE_FORMAT", lit(format))


def year(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.Year)


def quarter(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "QUARTER")


def month(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.Month)


def dayofweek(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "DAYOFWEEK")


def dayofmonth(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "DAYOFMONTH")


def dayofyear(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "DAYOFYEAR")


def hour(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "HOUR")


def minute(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "MINUTE")


def second(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "SECOND")


def weekofyear(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "WEEKOFYEAR")


def make_date(year: ColumnOrName, month: ColumnOrName, day: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(year, "MAKE_DATE", month, day)


def date_add(col: ColumnOrName, days: t.Union[ColumnOrName, int]) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.DateAdd, expression=Column.ensure_col(days).expression)


def date_sub(col: ColumnOrName, days: t.Union[ColumnOrName, int]) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.DateSub, expression=Column.ensure_col(days).expression)


def date_diff(end: ColumnOrName, start: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(end, glotexp.DateDiff, expression=Column.ensure_col(start).expression)


def add_months(start: ColumnOrName, months: t.Union[ColumnOrName, int]) -> Column:
    return Column.invoke_anonymous_function(start, "ADD_MONTHS", months)


def months_between(date1: ColumnOrName, date2: ColumnOrName, roundOff: t.Optional[bool] = None) -> Column:
    if roundOff is None:
        return Column.invoke_anonymous_function(date1, "MONTHS_BETWEEN", date2)
    return Column.invoke_anonymous_function(date1, "MONTHS_BETWEEN", date2, roundOff)


def to_date(col: ColumnOrName, format: t.Optional[str] = None) -> Column:
    if format is not None:
        return Column.invoke_anonymous_function(col, "TO_DATE", lit(format))
    return Column.invoke_anonymous_function(col, "TO_DATE")


def to_timestamp(col: ColumnOrName, format: t.Optional[str] = None) -> Column:
    if format is not None:
        return Column.invoke_anonymous_function(col, "TO_TIMESTAMP", lit(format))
    return Column.invoke_anonymous_function(col, "TO_TIMESTAMP")


def trunc(col: ColumnOrName, format: str) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.DateTrunc, unit=lit(format).expression)


def date_trunc(format: str, timestamp: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(timestamp, glotexp.TimestampTrunc, unit=lit(format).expression)


def next_day(col: ColumnOrName, dayOfWeek: str) -> Column:
    return Column.invoke_anonymous_function(col, "NEXT_DAY", lit(dayOfWeek))


def last_day(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "LAST_DAY")


def from_unixtime(col: ColumnOrName, format: str = None) -> Column:
    if format is not None:
        return Column.invoke_anonymous_function(col, "FROM_UNIXTIME", lit(format))
    return Column.invoke_anonymous_function(col, "FROM_UNIXTIME")


def unix_timestamp(timestamp: t.Optional[ColumnOrName] = None, format: str = None) -> Column:
    if format is not None:
        return Column.invoke_anonymous_function(timestamp, "UNIX_TIMESTAMP", lit(format))
    return Column.invoke_anonymous_function(timestamp, "UNIX_TIMESTAMP")


def from_utc_timestamp(timestamp: ColumnOrName, tz: ColumnOrName) -> Column:
    tz = tz if isinstance(tz, Column) else lit(tz)
    return Column.invoke_anonymous_function(timestamp, "FROM_UTC_TIMESTAMP", tz)


def to_utc_timestamp(timestamp: ColumnOrName, tz: ColumnOrName) -> Column:
    tz = tz if isinstance(tz, Column) else lit(tz)
    return Column.invoke_anonymous_function(timestamp, "TO_UTC_TIMESTAMP", tz)


def timestamp_seconds(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "TIMESTAMP_SECONDS")


def window(
    timeColumn: ColumnOrName,
    windowDuration: str,
    slideDuration: t.Optional[str] = None,
    startTime: t.Optional[str] = None,
) -> Column:
    if slideDuration is not None and startTime is not None:
        return Column.invoke_anonymous_function(
            timeColumn, "WINDOW", lit(windowDuration), lit(slideDuration), lit(startTime)
        )
    if slideDuration is not None:
        return Column.invoke_anonymous_function(timeColumn, "WINDOW", lit(windowDuration), lit(slideDuration))
    if startTime is not None:
        return Column.invoke_anonymous_function(
            timeColumn, "WINDOW", lit(windowDuration), lit(windowDuration), lit(startTime)
        )
    return Column.invoke_anonymous_function(timeColumn, "WINDOW", lit(windowDuration))


def session_window(timeColumn: ColumnOrName, gapDuration: ColumnOrName) -> Column:
    gapDuration = gapDuration if isinstance(gapDuration, Column) else lit(gapDuration)
    return Column.invoke_anonymous_function(timeColumn, "SESSION_WINDOW", gapDuration)


def crc32(col: ColumnOrName) -> Column:
    col = col if isinstance(col, Column) else lit(col)
    return Column.invoke_anonymous_function(col, "CRC32")


def md5(col: ColumnOrName) -> Column:
    col = col if isinstance(col, Column) else lit(col)
    return Column.invoke_anonymous_function(col, "MD5")


def sha1(col: ColumnOrName) -> Column:
    col = col if isinstance(col, Column) else lit(col)
    return Column.invoke_anonymous_function(col, "SHA1")


def sha2(col: ColumnOrName, numBits: int) -> Column:
    col = col if isinstance(col, Column) else lit(col)
    return Column.invoke_anonymous_function(col, "SHA2", numBits)


def hash(*cols: ColumnOrName) -> Column:
    args = cols[1:] if len(cols) > 1 else []
    return Column.invoke_anonymous_function(cols[0], "HASH", *args)


def xxhash64(*cols: ColumnOrName) -> Column:
    args = cols[1:] if len(cols) > 1 else []
    return Column.invoke_anonymous_function(cols[0], "XXHASH64", *args)


def assert_true(col: ColumnOrName, errorMsg: t.Optional[ColumnOrName] = None) -> Column:
    if errorMsg is not None:
        errorMsg = errorMsg if isinstance(errorMsg, Column) else lit(errorMsg)
        return Column.invoke_anonymous_function(col, "ASSERT_TRUE", errorMsg)
    return Column.invoke_anonymous_function(col, "ASSERT_TRUE")


def raise_error(errorMsg: ColumnOrName) -> Column:
    errorMsg = errorMsg if isinstance(errorMsg, Column) else lit(errorMsg)
    return Column.invoke_anonymous_function(errorMsg, "RAISE_ERROR")


def upper(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.Upper)


def lower(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.Lower)


def ascii(col: ColumnOrPrimitive) -> Column:
    return Column.invoke_anonymous_function(col, "ASCII")


def base64(col: ColumnOrPrimitive) -> Column:
    return Column.invoke_anonymous_function(col, "BASE64")


def unbase64(col: ColumnOrPrimitive) -> Column:
    return Column.invoke_anonymous_function(col, "UNBASE64")


def ltrim(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "LTRIM")


def rtrim(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "RTRIM")


def trim(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "TRIM")


def concat_ws(sep: str, *cols: ColumnOrName) -> Column:
    cols = [Column(col) for col in cols]
    return Column.invoke_expression_over_column(
        None, glotexp.ConcatWs, expressions=[x.expression for x in [lit(sep)] + list(cols)]
    )


def decode(col: ColumnOrName, charset: str) -> Column:
    return Column.invoke_anonymous_function(col, "DECODE", lit(charset))


def encode(col: ColumnOrName, charset: str) -> Column:
    return Column.invoke_anonymous_function(col, "ENCODE", lit(charset))


def format_number(col: ColumnOrName, d: int) -> Column:
    return Column.invoke_anonymous_function(col, "FORMAT_NUMBER", lit(d))


def format_string(format: str, *cols: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(lit(format), "FORMAT_STRING", *cols)


def instr(col: ColumnOrName, substr: str) -> Column:
    return Column.invoke_anonymous_function(col, "INSTR", lit(substr))


def overlay(
    src: ColumnOrName, replace: ColumnOrName, pos: t.Union[ColumnOrName, int], len: t.Union[ColumnOrName, int] = None
) -> Column:
    if len is not None:
        return Column.invoke_anonymous_function(src, "OVERLAY", replace, pos, len)
    return Column.invoke_anonymous_function(src, "OVERLAY", replace, pos)


def sentences(
    string: ColumnOrName, language: t.Optional[ColumnOrName] = None, country: t.Optional[ColumnOrName] = None
) -> Column:
    if language is not None and country is not None:
        return Column.invoke_anonymous_function(string, "SENTENCES", language, country)
    if language is not None:
        return Column.invoke_anonymous_function(string, "SENTENCES", language)
    if country is not None:
        return Column.invoke_anonymous_function(string, "SENTENCES", lit("en"), country)
    return Column.invoke_anonymous_function(string, "SENTENCES")


def substring(str: ColumnOrName, pos: int, len: int) -> Column:
    return Column.ensure_col(str).substr(pos, len)


def substring_index(str: ColumnOrName, delim: str, count: int) -> Column:
    return Column.invoke_anonymous_function(str, "SUBSTRING_INDEX", lit(delim), lit(count))


def levenshtein(left: ColumnOrName, right: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(
        left, glotexp.Levenshtein, expression=Column.ensure_col(right).expression
    )


def locate(substr: str, str: ColumnOrName, pos: int = None) -> Column:
    if pos is not None:
        return Column.invoke_anonymous_function(lit(substr), "LOCATE", str, lit(pos))
    return Column.invoke_anonymous_function(lit(substr), "LOCATE", str)


def lpad(col: ColumnOrName, len: int, pad: str) -> Column:
    return Column.invoke_anonymous_function(col, "LPAD", lit(len), lit(pad))


def rpad(col: ColumnOrName, len: int, pad: str) -> Column:
    return Column.invoke_anonymous_function(col, "RPAD", lit(len), lit(pad))


def repeat(col: ColumnOrName, n: int) -> Column:
    return Column.invoke_anonymous_function(col, "REPEAT", n)


def split(str: ColumnOrName, pattern: str, limit: t.Optional[int] = None) -> Column:
    if limit is not None:
        return Column.invoke_expression_over_column(
            str, glotexp.Split, expression=lit(pattern).expression, limit=lit(limit).expression
        )
    return Column.invoke_expression_over_column(str, glotexp.Split, expression=lit(pattern).expression)


def regexp_extract(str: ColumnOrName, pattern: str, idx: t.Optional[int] = None) -> Column:
    if idx is not None:
        return Column.invoke_anonymous_function(str, "REGEXP_EXTRACT", lit(pattern), idx)
    return Column.invoke_anonymous_function(str, "REGEXP_EXTRACT", lit(pattern))


def regexp_replace(str: ColumnOrName, pattern: str, replacement: str) -> Column:
    return Column.invoke_anonymous_function(str, "REGEXP_REPLACE", lit(pattern), lit(replacement))


def initcap(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.Initcap)


def soundex(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "SOUNDEX")


def bin(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "BIN")


def hex(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "HEX")


def unhex(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "UNHEX")


def length(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.Length)


def octet_length(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "OCTET_LENGTH")


def bit_length(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "BIT_LENGTH")


def translate(srcCol: ColumnOrName, matching: str, replace: str) -> Column:
    return Column.invoke_anonymous_function(srcCol, "TRANSLATE", lit(matching), lit(replace))


def array(*cols: t.Union[ColumnOrName, t.Iterable[ColumnOrName]]) -> Column:
    cols = _flatten(cols) if not isinstance(cols[0], (str, Column)) else cols
    cols = [Column.ensure_col(col).expression for col in cols]
    return Column.invoke_expression_over_column(None, glotexp.Array, expressions=cols)


def create_map(*cols: t.Union[ColumnOrName, t.Iterable[ColumnOrName]]) -> Column:
    cols = list(_flatten(cols)) if not isinstance(cols[0], (str, Column)) else cols
    return Column.invoke_expression_over_column(
        None, glotexp.Map, keys=array(cols[::2]).expression, values=array(cols[1::2]).expression
    )


def map_from_arrays(col1: ColumnOrName, col2: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col1, "MAP_FROM_ARRAYS", col2)


def array_contains(col: ColumnOrName, value: ColumnOrPrimitive) -> Column:
    value = value if isinstance(value, Column) else lit(value)
    return Column.invoke_expression_over_column(col, glotexp.ArrayContains, expression=value.expression)


def arrays_overlap(col1: ColumnOrName, col2: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col1, "ARRAYS_OVERLAP", Column.ensure_col(col2))


def slice(x: ColumnOrName, start: t.Union[ColumnOrName, int], length: t.Union[ColumnOrName, int]) -> Column:
    start = start if isinstance(start, Column) else lit(start)
    length = length if isinstance(length, Column) else lit(length)
    return Column.invoke_anonymous_function(x, "SLICE", start, length)


def array_join(col: ColumnOrName, delimiter: str, null_replacement: t.Optional[str] = None) -> Column:
    if null_replacement is not None:
        return Column.invoke_anonymous_function(col, "ARRAY_JOIN", lit(delimiter), lit(null_replacement))
    return Column.invoke_anonymous_function(col, "ARRAY_JOIN", lit(delimiter))


def concat(*cols: ColumnOrName) -> Column:
    if len(cols) == 1:
        return Column.invoke_anonymous_function(cols[0], "CONCAT")
    return Column.invoke_anonymous_function(cols[0], "CONCAT", *[Column.ensure_col(x).expression for x in cols[1:]])


def array_position(col: ColumnOrName, value: ColumnOrPrimitive) -> Column:
    value = value if isinstance(value, Column) else lit(value)
    return Column.invoke_anonymous_function(col, "ARRAY_POSITION", value)


def element_at(col: ColumnOrName, value: ColumnOrPrimitive) -> Column:
    value = value if isinstance(value, Column) else lit(value)
    return Column.invoke_anonymous_function(col, "ELEMENT_AT", value)


def array_remove(col: ColumnOrName, value: ColumnOrPrimitive) -> Column:
    value = value if isinstance(value, Column) else lit(value)
    return Column.invoke_anonymous_function(col, "ARRAY_REMOVE", value)


def array_distinct(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "ARRAY_DISTINCT")


def array_intersect(col1: ColumnOrName, col2: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col1, "ARRAY_INTERSECT", Column.ensure_col(col2))


def array_union(col1: ColumnOrName, col2: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col1, "ARRAY_UNION", Column.ensure_col(col2))


def array_except(col1: ColumnOrName, col2: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col1, "ARRAY_EXCEPT", Column.ensure_col(col2))


def explode(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.Explode)


def posexplode(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.Posexplode)


def explode_outer(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "EXPLODE_OUTER")


def posexplode_outer(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "POSEXPLODE_OUTER")


def get_json_object(col: ColumnOrName, path: str) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.JSONExtract, path=lit(path).expression)


def json_tuple(col: ColumnOrName, *fields: str) -> Column:
    return Column.invoke_anonymous_function(col, "JSON_TUPLE", *[lit(field) for field in fields])


def from_json(
    col: ColumnOrName,
    schema: t.Union[Column, str],
    options: t.Optional[t.Dict[str, str]] = None,
) -> Column:
    schema = schema if isinstance(schema, Column) else lit(schema)
    if options is not None:
        options = create_map([lit(x) for x in _flatten(options.items())])
        return Column.invoke_anonymous_function(col, "FROM_JSON", schema, options)
    return Column.invoke_anonymous_function(col, "FROM_JSON", schema)


def to_json(col: ColumnOrName, options: t.Optional[t.Dict[str, str]] = None) -> Column:
    if options is not None:
        options = create_map([lit(x) for x in _flatten(options.items())])
        return Column.invoke_anonymous_function(col, "TO_JSON", options)
    return Column.invoke_anonymous_function(col, "TO_JSON")


def schema_of_json(col: ColumnOrName, options: t.Optional[t.Dict[str, str]] = None) -> Column:
    if options is not None:
        options = create_map([lit(x) for x in _flatten(options.items())])
        return Column.invoke_anonymous_function(col, "SCHEMA_OF_JSON", options)
    return Column.invoke_anonymous_function(col, "SCHEMA_OF_JSON")


def schema_of_csv(col: ColumnOrName, options: t.Optional[t.Dict[str, str]] = None) -> Column:
    if options is not None:
        options = create_map([lit(x) for x in _flatten(options.items())])
        return Column.invoke_anonymous_function(col, "SCHEMA_OF_CSV", options)
    return Column.invoke_anonymous_function(col, "SCHEMA_OF_CSV")


def to_csv(col: ColumnOrName, options: t.Optional[t.Dict[str, str]] = None) -> Column:
    if options is not None:
        options = create_map([lit(x) for x in _flatten(options.items())])
        return Column.invoke_anonymous_function(col, "TO_CSV", options)
    return Column.invoke_anonymous_function(col, "TO_CSV")


def size(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "SIZE")


def array_min(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "ARRAY_MIN")


def array_max(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "ARRAY_MAX")


def sort_array(col: ColumnOrName, asc: t.Optional[bool] = None) -> Column:
    if asc is not None:
        return Column.invoke_anonymous_function(col, "SORT_ARRAY", lit(asc))
    return Column.invoke_anonymous_function(col, "SORT_ARRAY")


def array_sort(col: ColumnOrName) -> Column:
    return Column.invoke_expression_over_column(col, glotexp.ArraySort)


def shuffle(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "SHUFFLE")


def reverse(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "REVERSE")


def flatten(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "FLATTEN")


def map_keys(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "MAP_KEYS")


def map_values(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "MAP_VALUES")


def map_entries(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "MAP_ENTRIES")


def map_from_entries(col: ColumnOrName) -> Column:
    return Column.invoke_anonymous_function(col, "MAP_FROM_ENTRIES")


def array_repeat(col: ColumnOrName, count: t.Union[ColumnOrName, int]) -> Column:
    count = count if isinstance(count, Column) else lit(count)
    return Column.invoke_anonymous_function(col, "ARRAY_REPEAT", count)


def array_zip(*cols: ColumnOrName) -> Column:
    if len(cols) == 1:
        return Column.invoke_anonymous_function(cols[0], "ARRAY_ZIP")
    return Column.invoke_anonymous_function(cols[0], "ARRAY_ZIP", *cols[1:])


def map_concat(*cols: t.Union[ColumnOrName, t.Iterable[ColumnOrName]]) -> Column:
    cols = list(flatten(cols)) if not isinstance(cols[0], (str, Column)) else cols
    if len(cols) == 1:
        return Column.invoke_anonymous_function(cols[0], "MAP_CONCAT")
    return Column.invoke_anonymous_function(cols[0], "MAP_CONCAT", *cols[1:])


def sequence(start: ColumnOrName, stop: ColumnOrName, step: t.Optional[ColumnOrName] = None) -> Column:
    if step is not None:
        return Column.invoke_anonymous_function(start, "SEQUENCE", stop, step)
    return Column.invoke_anonymous_function(start, "SEQUENCE", stop)


def from_csv(
    col: ColumnOrName,
    schema: t.Union[Column, str],
    options: t.Optional[t.Dict[str, str]] = None,
) -> Column:
    schema = schema if isinstance(schema, Column) else lit(schema)
    if options is not None:
        options = create_map([lit(x) for x in _flatten(options.items())])
        return Column.invoke_anonymous_function(col, "FROM_CSV", schema, options)
    return Column.invoke_anonymous_function(col, "FROM_CSV", schema)


def aggregate(
    col: ColumnOrName,
    initialValue: ColumnOrName,
    merge: t.Callable[[Column, Column], Column],
    finish: t.Optional[t.Callable[[Column], Column]] = None,
    accumulator_name: str = "acc",
    target_row_name: str = "x",
) -> Column:
    merge_exp = glotexp.Lambda(
        this=merge(Column(accumulator_name), Column(target_row_name)).expression,
        expressions=[glotexp.to_identifier(accumulator_name, quoted=_lambda_quoted(accumulator_name)), glotexp.to_identifier(target_row_name, quoted=_lambda_quoted(target_row_name))],
    )
    if finish is not None:
        finish_exp = glotexp.Lambda(
            this=finish(Column(accumulator_name)).expression, expressions=[glotexp.to_identifier(accumulator_name, quoted=_lambda_quoted(accumulator_name))]
        )
        return Column.invoke_anonymous_function(col, "AGGREGATE", initialValue, Column(merge_exp), Column(finish_exp))
    return Column.invoke_anonymous_function(col, "AGGREGATE", initialValue, Column(merge_exp))


def transform(
    col: ColumnOrName,
    f: t.Union[t.Callable[[Column], Column], t.Callable[[Column, Column], Column]],
    target_row_name: str = "x",
    row_count_name: str = "i",
) -> Column:
    num_arguments = len(signature(f).parameters)
    expressions = [glotexp.to_identifier(target_row_name, quoted=_lambda_quoted(target_row_name))]
    columns = [Column(target_row_name)]
    if num_arguments > 1:
        columns.append(Column(row_count_name))
        expressions.append(glotexp.to_identifier(row_count_name, quoted=_lambda_quoted(row_count_name)))

    f_expression = glotexp.Lambda(this=f(*columns).expression, expressions=expressions)
    return Column.invoke_anonymous_function(col, "TRANSFORM", Column(f_expression))


def exists(col: ColumnOrName, f: t.Callable[[Column], Column], target_row_name: str = "x") -> Column:
    f_expression = glotexp.Lambda(
        this=f(Column(target_row_name)).expression, expressions=[glotexp.to_identifier(target_row_name, quoted=_lambda_quoted(target_row_name))]
    )
    return Column.invoke_anonymous_function(col, "EXISTS", Column(f_expression))


def forall(col: ColumnOrName, f: t.Callable[[Column], Column], target_row_name: str = "x") -> Column:
    f_expression = glotexp.Lambda(
        this=f(Column(target_row_name)).expression, expressions=[glotexp.to_identifier(target_row_name, quoted=_lambda_quoted(target_row_name))]
    )

    return Column.invoke_anonymous_function(col, "FORALL", Column(f_expression))


def filter(
    col: ColumnOrName,
    f: t.Union[t.Callable[[Column], Column], t.Callable[[Column, Column], Column]],
    target_row_name: str = "x",
    row_count_name: str = "i",
) -> Column:
    num_arguments = len(signature(f).parameters)
    expressions = [glotexp.to_identifier(target_row_name, quoted=_lambda_quoted(target_row_name))]
    columns = [Column(target_row_name)]
    if num_arguments > 1:
        columns.append(Column(row_count_name))
        expressions.append(glotexp.to_identifier(row_count_name, quoted=_lambda_quoted(row_count_name)))

    f_expression = glotexp.Lambda(this=f(*columns).expression, expressions=expressions)
    return Column.invoke_anonymous_function(col, "FILTER", Column(f_expression))


def zip_with(
    left: ColumnOrName,
    right: ColumnOrName,
    f: t.Callable[[Column, Column], Column],
    left_name: str = "x",
    right_name: str = "y",
) -> Column:
    f_expression = glotexp.Lambda(
        this=f(Column(left_name), Column(right_name)).expression,
        expressions=[glotexp.to_identifier(left_name, quoted=_lambda_quoted(left_name)), glotexp.to_identifier(right_name, quoted=_lambda_quoted(right_name))],
    )

    return Column.invoke_anonymous_function(left, "ZIP_WITH", right, Column(f_expression))


def transform_keys(
    col: ColumnOrName, f: t.Union[t.Callable[[Column, Column], Column]], key_name: str = "k", value_name: str = "v"
) -> Column:
    f_expression = glotexp.Lambda(
        this=f(Column(key_name), Column(value_name)).expression,
        expressions=[glotexp.to_identifier(key_name, quoted=_lambda_quoted(key_name)), glotexp.to_identifier(value_name, quoted=_lambda_quoted(value_name))],
    )
    return Column.invoke_anonymous_function(col, "TRANSFORM_KEYS", Column(f_expression))


def transform_values(
    col: ColumnOrName, f: t.Union[t.Callable[[Column, Column], Column]], key_name: str = "k", value_name: str = "v"
) -> Column:
    f_expression = glotexp.Lambda(
        this=f(Column(key_name), Column(value_name)).expression,
        expressions=[glotexp.to_identifier(key_name, quoted=_lambda_quoted(key_name)), glotexp.to_identifier(value_name, quoted=_lambda_quoted(value_name))],
    )
    return Column.invoke_anonymous_function(col, "TRANSFORM_VALUES", Column(f_expression))


def map_filter(
    col: ColumnOrName, f: t.Union[t.Callable[[Column, Column], Column]], key_name: str = "k", value_name: str = "v"
) -> Column:
    f_expression = glotexp.Lambda(
        this=f(Column(key_name), Column(value_name)).expression,
        expressions=[glotexp.to_identifier(key_name, quoted=_lambda_quoted(key_name)), glotexp.to_identifier(value_name, quoted=_lambda_quoted(value_name))],
    )
    return Column.invoke_anonymous_function(col, "MAP_FILTER", Column(f_expression))


def map_zip_with(
    col1: ColumnOrName,
    col2: ColumnOrName,
    f: t.Union[t.Callable[[Column, Column, Column], Column]],
    key_name: str = "k",
    value1: str = "v1",
    value2: str = "v2",
) -> Column:
    f_expression = glotexp.Lambda(
        this=f(Column(key_name), Column(value1), Column(value2)).expression,
        expressions=[
            glotexp.to_identifier(key_name, quoted=_lambda_quoted(key_name)),
            glotexp.to_identifier(value1, quoted=_lambda_quoted(value1)),
            glotexp.to_identifier(value2, quoted=_lambda_quoted(value2)),
        ],
    )
    return Column.invoke_anonymous_function(col1, "MAP_ZIP_WITH", col2, Column(f_expression))


def _lambda_quoted(value: str) -> t.Optional[bool]:
    return False if value == "_" else None
